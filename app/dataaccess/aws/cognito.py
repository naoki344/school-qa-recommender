from logging import Logger

import boto3


class CognitoClient:
    def __init__(self, user_pool_id: str, logger: Logger):
        self.logger = logger
        self.user_pool_id = user_pool_id
        self.client = boto3.client('cognito-idp')

    def admin_get_user(self, user_name: str):
        return self.client.admin_get_user(UserPoolId=self.user_pool_id,
                                          Username=user_name)
