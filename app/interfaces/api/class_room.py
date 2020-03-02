import json
from logging import getLogger

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.application.usecase.class_room import ApproveJoinClassRoomRequest
from app.application.usecase.class_room import CreateClassRoom
from app.application.usecase.class_room import FindClassRoom
from app.application.usecase.class_room import RequestJoinClassRoom
from app.configure.usecase.class_room import approve_join_class_room_request
from app.configure.usecase.class_room import create_class_room
from app.configure.usecase.class_room import find_class_room
from app.configure.usecase.class_room import request_join_class_room
from app.interfaces.api.response import APIGatewayResponse
from app.model.class_room.class_room import ClassRoomId
from app.model.user.user import UserId


def create_class_room_handler(event, context):
    data = json.loads(event["body"])
    service: CreateClassRoom = create_class_room(logger=getLogger())
    user_id = AuthenticationEventPerser.parse(event)
    class_room = service.run(user_id, data)
    return APIGatewayResponse.to_response({"class_room": class_room.to_dict()})


def find_class_room_handler(event, context):
    path = event["pathParameters"]
    class_room_id = ClassRoomId(int(path["class_room_id"]))
    logger = getLogger()
    service: FindClassRoom = find_class_room(logger=logger)
    class_room, student_list = service.run(class_room_id)
    return APIGatewayResponse.to_response({
        "class_room":
        class_room.to_dict(),
        "student_list":
        student_list.to_list()
    })


def request_join_class_room_handler(event, context):
    path = event["pathParameters"]
    class_room_id = ClassRoomId(int(path["class_room_id"]))
    user_id = AuthenticationEventPerser.parse(event)
    logger = getLogger()
    service: RequestJoinClassRoom = request_join_class_room(logger=logger)
    student = service.run(user_id, class_room_id)
    return APIGatewayResponse.to_response({"student": student.to_dict()})


def approve_join_class_room_request_handler(event, context):
    user_id = AuthenticationEventPerser.parse(event)
    logger = getLogger()
    path = event["pathParameters"]
    class_room_id = ClassRoomId(int(path["class_room_id"]))
    data = json.loads(event["body"])
    approve_user_list = data.get('approve_user_list')
    if not approve_user_list:
        raise Exception('accept_user_list is required.')

    service: ApproveJoinClassRoomRequest = approve_join_class_room_request(
        logger=logger)
    service.run(user_id, class_room_id, [UserId(d) for d in approve_user_list])
    return APIGatewayResponse.to_response({})
