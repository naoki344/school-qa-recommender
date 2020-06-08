import datetime


def create_cognito_user():
    return {
        'Username':
        '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
        'UserAttributes': [{
            'Name': 'sub',
            'Value': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }, {
            'Name': 'custom:last_name',
            'Value': '三好'
        }, {
            'Name': 'email_verified',
            'Value': 'true'
        }, {
            'Name': 'custom:last_name_kana',
            'Value': 'ミヨシ'
        }, {
            'Name': 'custom:first_name',
            'Value': '直紀'
        }, {
            'Name': 'nickname',
            'Value': 'Naoki'
        }, {
            'Name': 'email',
            'Value': 'trombone344@gmail.com'
        }, {
            'Name': 'custom:first_name_kana',
            'Value': 'ナオキ'
        }],
        'UserCreateDate':
        datetime.datetime(2020, 2, 26, 0, 18, 16, 874000),
        'UserLastModifiedDate':
        datetime.datetime(2020, 2, 26, 0, 20, 14, 702000),
        'Enabled':
        True,
        'UserStatus':
        'CONFIRMED',
        'ResponseMetadata': {
            'RequestId': '1569e7ab-6a45-4d6c-af01-59e64280c7c9',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'date': 'Wed, 26 Feb 2020 14:11:41 GMT',
                'content-type': 'application/x-amz-json-1.1',
                'content-length': '570',
                'connection': 'keep-alive',
                'x-amzn-requestid': '1569e7ab-6a45-4d6c-af01-59e64280c7c9'
            },
            'RetryAttempts': 0
        }
    }
