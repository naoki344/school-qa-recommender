from logging import Logger

from app.dataaccess.user import UserDatasource
from app.model.user.user import User
from app.model.user.user import UserId


class UserQueryService:
    def __init__(self, datasource: UserDatasource, logger: Logger):
        self.datasource = datasource

    def find(self, user_id: UserId) -> User:
        return self.datasource.find(user_id)
