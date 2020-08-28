import json
import logging

import boto3
import requests
from requests_aws_sign import AWSV4Sign
from warrant.aws_srp import AWSSRP

USERNAME = 'trombone344@gmail.com'
PASSWORD = '@Naoki007744'
ACCOUNT_ID = "663456595771"
REGION = "ap-northeast-1"
API_ENDPOINT = "https://y88wcno7sl.execute-api.ap-northeast-1.amazonaws.com/devmiyoshi"
USER_POOL_ID = "ap-northeast-1_1G6B3pml2"
CLIENT_ID = "6mk3tldtr55q0oc0ime00b90k1"
IDENTITY_POOL_ID = "ap-northeast-1:06e7fa0c-c982-4e43-905f-dbb35de65387"


def main():
    aws = AWSSRP(username=USERNAME, password=PASSWORD,
                 pool_id=USER_POOL_ID, client_id=CLIENT_ID)
    tokens = aws.authenticate_user()
    id_token = tokens['AuthenticationResult']['IdToken']

    logins = {'cognito-idp.' + REGION +
              '.amazonaws.com/' + USER_POOL_ID: id_token}
    client = boto3.client('cognito-identity', region_name=REGION)
    cognito_identity_id = client.get_id(
        AccountId=ACCOUNT_ID,
        IdentityPoolId=IDENTITY_POOL_ID,
        Logins=logins
    )
    id_credentials = client.get_credentials_for_identity(
        IdentityId=cognito_identity_id['IdentityId'],
        Logins=logins
    )

    session = boto3.session.Session(
        aws_access_key_id=id_credentials['Credentials']['AccessKeyId'],
        aws_secret_access_key=id_credentials['Credentials']['SecretKey'],
        aws_session_token=id_credentials['Credentials']['SessionToken'],
        region_name=REGION
    )
    credentials = session.get_credentials()
    service = 'execute-api'
    headers = {"Content-Type": "application/json"}
    request_path = '/classroom/18'
    get_by_id_url = API_ENDPOINT + request_path

    auth = AWSV4Sign(credentials, REGION, service)
    # GET
    response = requests.request(
        'GET', get_by_id_url, auth=auth, headers=headers)
    print(response.text)

    data = json.dumps({
            'name': 'test name',
            'image_url': 'https://example.example.com/test.jpg',
            'publish_type': 'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity': 10,
            'caption': 'test caption'
        }
            )
    create_url = API_ENDPOINT + '/classroom'
    response = requests.post(create_url, auth=auth, headers=headers, data=data)
    res = json.loads(response.text)
    classroom_id = res["classroom"]["classroom_id"]
    print(response.text)

    #POST request
    create_url = API_ENDPOINT + f'/classroom/{classroom_id}/invite_key'
    response = requests.post(create_url, auth=auth, headers=headers, data={})
    invite_key = json.loads(response.text)["classmate_invite"]["invite_key"]
    print(response.text)

    #GET request
    create_url = API_ENDPOINT + f'/invite_key/{invite_key}/classroom'
    response = requests.get(create_url, auth=auth, headers=headers, data='')
    print(response.text)

    #POST request
    create_url = API_ENDPOINT + f'/invite_key/{invite_key}/join_request'
    response = requests.post(create_url, auth=auth, headers=headers, data={})
    print(response.text)

    #GET request
    create_url = API_ENDPOINT + f'/classroom/my_classroom'
    response = requests.get(create_url, auth=auth, headers=headers, data='')
    print(response.text)


if __name__ == '__main__':
    main()

