from typing import Any
from typing import Optional

import pytz
from tzlocal import get_localzone

from app.model.user.user import CognitoUserSub
from app.model.user.user import Email
from app.model.user.user import FirstName
from app.model.user.user import FirstNameKana
from app.model.user.user import LastName
from app.model.user.user import LastNameKana
from app.model.user.user import Nickname
from app.model.user.user import RegisterDate
from app.model.user.user import User
from app.model.user.user import UserId
from app.model.user.user import UserName


class AuthenticationEventPerser:
    def parse(event: dict) -> UserId:
        auth_provider = event['requestContext']['identity'][
            'cognitoAuthenticationProvider']
        cognito_user_id = auth_provider.split(":CognitoSignIn:")[-1]
        return UserId(cognito_user_id)


class CognitoUserParser:
    def parse(cognito: dict) -> User:
        def get_att(key: str, _type: type) -> Optional[Any]:
            attributes = cognito['UserAttributes']
            data = next(filter(lambda i: i['Name'] == key, attributes), None)
            if data.get('Value'):
                return _type(data.get('Value'))
            return None

        def get_date(key: str):
            date = cognito[key].astimezone(get_localzone())
            date = date.astimezone(pytz.timezone('Asia/Tokyo'))
            return date

        return User(user_id=UserId(cognito['Username']),
                    nickname=get_att('nickname', Nickname),
                    user_name=UserName(
                        first_name=get_att('custom:first_name', FirstName),
                        last_name=get_att('custom:last_name', LastName)),
                    email=get_att('email', Email),
                    register_date=RegisterDate(get_date('UserCreateDate')),
                    cognito_user_sub=get_att('sub', CognitoUserSub))
