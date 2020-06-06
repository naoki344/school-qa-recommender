import io
import mimetypes
import os

from PIL import Image

from app.dataaccess.aws.s3_file import S3FileClient


def s3_event_create_image_thumbnail_handler(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    s3_key = event["Records"][0]["s3"]["object"]["key"]
    s3_file_client = S3FileClient(bucket_name)
    image = Image.open(s3_file_client.get_fp(s3_key))
    content_type = mimetypes.guess_type(s3_key)[0]

    # tobytes
    img = io.BytesIO()
    img_h60 = __convert_with_height(image=image, new_height=60)
    img_h60.save(img, image.format)
    s3_file_client.upload_file(s3_key=__get_s3_key("h60", s3_key),
                               data=img.getvalue(),
                               content_type=content_type)

    img = io.BytesIO()
    img_h180 = __convert_with_height(image=image, new_height=180)
    img_h180.save(img, image.format)
    s3_file_client.upload_file(s3_key=__get_s3_key("h180", s3_key),
                               data=img.getvalue(),
                               content_type=content_type)

    img = io.BytesIO()
    img_w512 = __convert_with_width(image=image, new_width=512)
    img_w512.save(img, image.format)
    s3_file_client.upload_file(s3_key=__get_s3_key("w512", s3_key),
                               data=img.getvalue(),
                               content_type=content_type)


def __convert_with_height(image: Image, new_height: int):
    if new_height >= image.height:
        return image
    return image.resize(
        (int(new_height / image.height * image.width), int(new_height)),
        Image.LANCZOS)


def __convert_with_width(image: Image, new_width: int):
    if new_width >= image.width:
        return image
    return image.resize(
        (int(new_width), int(new_width / image.width * image.height)),
        Image.LANCZOS)


def __get_s3_key(size_prefix: str, s3_key: str):
    path, name = os.path.split(s3_key)
    return os.path.join("public/thumbnail/", size_prefix, name)
