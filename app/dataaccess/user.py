from logging import Logger

from app.anticorruption.model.user.parser import CognitoUserParser
from app.dataaccess.aws.cognito import CognitoClient
from app.model.user.user import User
from app.model.user.user import UserId


class UserDatasource:
    def __init__(self, client: CognitoClient, logger: Logger) -> None:
        self.logger = logger
        self.client = client

    def find(self, user_id: UserId) -> User:
        data = self.client.admin_get_user(user_name=user_id.value)
        return CognitoUserParser.parse(data)
