from app.anticorruption.cognito import PostConfirmationTransfer
from app.dataaccess.s3_file import S3FileClient


def post_confirmation_handler(event, context):
    transfer = PostConfirmationTransfer(event)
    user_id = transfer.get_user_id()
    avatar_url = transfer.get_avatar_url()
    if avatar_url:
        s3_bucket_name, s3_key = avatar_url.get_s3_location()
        client = S3FileClient(s3_bucket_name)
        client.copy(s3_key, s3_bucket_name, f"user/{user_id}/avatar_image")
    return event
