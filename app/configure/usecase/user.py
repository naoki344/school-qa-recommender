from logging import Logger

from app.application.usecase.user import UploadUserAvatarImage
from app.configure.query.user import user_query_service
from app.configure.resoruce.s3 import s3_public_image_datasource


def upload_user_avatar_image(logger: Logger) -> UploadUserAvatarImage:
    return UploadUserAvatarImage(
        s3_public_image_datasource=s3_public_image_datasource(logger),
        user_service=user_query_service(logger),
        logger=logger)
