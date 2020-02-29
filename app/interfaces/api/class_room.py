import json
from logging import getLogger

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.application.usecase.class_room import CreateClassRoom
from app.application.usecase.class_room import FindClassRoom
from app.configure.usecase.class_room import create_class_room
from app.configure.usecase.class_room import find_class_room
from app.interfaces.api.response import APIGatewayResponse
from app.model.class_room.class_room import ClassRoomId


def create_class_room_handler(event, context):
    data = json.loads(event["body"])
    service: CreateClassRoom = create_class_room(logger=getLogger())
    user_id = AuthenticationEventPerser.parse(event)
    question = service.run(user_id, data)
    return APIGatewayResponse.to_response(question.to_dict())


def find_class_room_handler(event, context):
    path = event["pathParameters"]
    question_id = ClassRoomId(int(path["class_room_id"]))
    logger = getLogger()
    service: FindClassRoom = find_class_room(logger=logger)
    question = service.run(question_id)
    return APIGatewayResponse.to_response(question.to_dict())
