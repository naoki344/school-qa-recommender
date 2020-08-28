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
    auth = AWSV4Sign(credentials, REGION, service)

    request_path = f"/classroom/14/work/29/comment"
    url = API_ENDPOINT + request_path
    response = requests.get(url, auth=auth, headers=headers)
    print(response.text)

    request_path = f"/classroom/1/work"
    url = API_ENDPOINT + request_path
    response = requests.get(url, auth=auth, headers=headers)
    data = json.loads(response.text)
    work_id = data['work_list'][0]["work_id"]

    request_path = f"/classroom/1/work/{work_id}/comment"
    post_data = json.dumps({
            'comment_type': 'message',
            'parent_comment_id': 2,
            'body': 'comment body test'
    })
    url = API_ENDPOINT + request_path
    response = requests.post(url, auth=auth, headers=headers, data=post_data)
    print(response.text)

    request_path = f"/classroom/1/work/{work_id}/comment"
    response = requests.get(url, auth=auth, headers=headers)
    print(response.text)


if __name__ == '__main__':
    main()
