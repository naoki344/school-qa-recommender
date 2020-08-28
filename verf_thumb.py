from app.interfaces.s3.image_convert import s3_event_create_image_thumbnail_handler


data = {
    "Records": [
        {
            "s3": {
                "bucket": {"name": "devmiyoshi-toi-toy-private-image-storage"},
                "object": {"key": "public/upload/avatar_image.png"}
            }
        },
    ]
}
s3_event_create_image_thumbnail_handler(data, {})
