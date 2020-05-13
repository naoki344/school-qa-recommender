import base64
import uuid
from logging import Logger

from app.application.query.user import UserQueryService
from app.dataaccess.aws.s3_file import S3FileClient
from app.model.user.user import UserAvatarUrl


class UploadUserAvatarImage:
    def __init__(self, s3_public_image_datasource: S3FileClient,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.s3_datasource = s3_public_image_datasource
        self.user_service = user_service
        self.logger = logger

    def run(self, data: str) -> UserAvatarUrl:
        data_type, encoded_data = data.split(",", 1)
        imageBody = base64.b64decode(encoded_data)
        uuid_str = str(uuid.uuid4())
        url = self.s3_datasource.upload_file(f'UserAvatarImage/{uuid_str}',
                                             imageBody,
                                             data_type.split(":")[1])
        return UserAvatarUrl(url)
