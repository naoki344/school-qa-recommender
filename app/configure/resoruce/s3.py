import os
from logging import Logger
from app.dataaccess.aws.s3_file import S3FileClient

stage_name = os.environ['STAGE_NAME']


def create_s3_file_client(bucket_name: str, logger: Logger):
    return S3FileClient(bucket_name)


def s3_private_image_datasource(logger: Logger):
    return create_s3_file_client(
        f'{stage_name}-toi-toy-private-image-storage',
        logger)


def s3_public_image_datasource(logger: Logger):
    return create_s3_file_client(
        f'{stage_name}-toi-toy-public-image-storage',
        logger)
