import os
import random

from app.anticorruption.cognito import PostConfirmationTransfer
from app.dataaccess.s3_file import S3FileClient


def post_confirmation_handler(event, context):
    transfer = PostConfirmationTransfer(event)
    user_id = transfer.get_user_id()
    avatar_url = transfer.get_avatar_url()

    if avatar_url:
        s3_bucket_name, s3_key = avatar_url.get_s3_location()
    else:
        s3_bucket_name = os.environ['TOI_TOY_PUBLICK_BUCKET']
        default_images = [
            'UserAvatarImage/user-default-image-1.png',
            'UserAvatarImage/user-default-image-2.png',
            'UserAvatarImage/user-default-image-3.png'
        ]
        s3_key = random.choice(default_images)
    client = S3FileClient(s3_bucket_name)
    print(f"BucketName: {s3_bucket_name}, S3Key: {s3_key}")
    client.copy(s3_key, s3_bucket_name, f"user/{user_id}/avatar_image")
    return event
