import json
from logging import getLogger

from app.configure.usecase.user import upload_user_avatar_image
from app.interfaces.api.response import APIGatewayErrorResponse
from app.interfaces.api.response import APIGatewayResponse


def upload_user_avatar_image_handler(event, context):
    try:
        logger = getLogger()
        data = event["body"]
        service = upload_user_avatar_image(logger)
        url = service.run(data)
        return APIGatewayResponse.to_response({"avatar_url": url.value})
    except Exception as e:
        logger.error(e)
        return APIGatewayErrorResponse.to_response(e)
