import json
from logging import getLogger

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.interfaces.api.response import APIGatewayResponse
from app.configure.usecase.user import upload_user_avatar_image


def upload_user_avatar_image_handler(event, context):
    data = event["body"]
    service = upload_user_avatar_image(getLogger())
    url = service.run(data)

    return APIGatewayResponse.to_response(
            {"avatar_url": url.value})
