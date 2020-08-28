from app.dataaccess.user import UserDatasource
from app.dataaccess.aws.cognito import CognitoClient
from app.model.user.user import UserId


user_pool_id = 'ap-northeast-1_1G6B3pml2'
user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
dataaccess = UserDatasource(
        client=CognitoClient(user_pool_id=user_pool_id))
print(dataaccess.find(user_id=user_id).to_dict())
