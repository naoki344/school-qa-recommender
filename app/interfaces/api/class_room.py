import json
from logging import getLogger

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.application.usecase.class_room import CreateClassRoom
from app.configure.usecase.class_room import create_class_room
from app.interfaces.api.response import APIGatewayResponse


def create_class_room_handler(event, context):
    data = json.loads(event["body"])
    service: CreateClassRoom = create_class_room(logger=getLogger())
    user_id = AuthenticationEventPerser.parse(event)
    question = service.run(user_id, data)
    return APIGatewayResponse.to_response(question.to_dict())
