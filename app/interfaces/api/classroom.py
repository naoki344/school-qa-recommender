import json
from logging import getLogger

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.application.usecase.classroom import ApproveJoinClassroomRequest
from app.application.usecase.classroom import CreateClassmateInviteLink
from app.application.usecase.classroom import CreateClassroom
from app.application.usecase.classroom import FindClassroom
from app.application.usecase.classroom import FindClassroomByInviteKey
from app.application.usecase.classroom import RequestJoinClassroom
from app.configure.usecase.classroom import approve_join_classroom_request
from app.configure.usecase.classroom import create_classmate_invite_link
from app.configure.usecase.classroom import create_classroom
from app.configure.usecase.classroom import find_classroom
from app.configure.usecase.classroom import find_classroom_by_invite_key
from app.configure.usecase.classroom import get_my_classroom_list
from app.configure.usecase.classroom import request_join_classroom
from app.interfaces.api.response import APIGatewayResponse
from app.model.classroom.classroom import ClassroomId
from app.model.classroom.invite import InviteKey
from app.model.classroom.my_classroom import MyClassroomList
from app.model.user.user import UserId


def create_classroom_handler(event, context):
    data = json.loads(event["body"])
    service: CreateClassroom = create_classroom(logger=getLogger())
    user_id = AuthenticationEventPerser.parse(event)
    classroom = service.run(user_id, data)
    return APIGatewayResponse.to_response({"classroom": classroom.to_dict()})


def find_classroom_handler(event, context):
    user_id = AuthenticationEventPerser.parse(event)
    path = event["pathParameters"]
    classroom_id = ClassroomId(int(path["classroom_id"]))
    logger = getLogger()
    service: FindClassroom = find_classroom(logger=logger)
    classroom, classmate_list = service.run(user_id, classroom_id)
    return APIGatewayResponse.to_response({
        "classroom":
        classroom.to_dict(),
        "classmate_list":
        classmate_list.to_list()
    })


def find_classroom_by_invite_key_handler(event, context):
    user_id = AuthenticationEventPerser.parse(event)
    path = event["pathParameters"]
    logger = getLogger()
    invite_key = InviteKey(str(path["invite_key"]))
    service: FindClassroomByInviteKey = find_classroom_by_invite_key(
        logger=logger)
    classroom = service.run(user_id, invite_key)
    return APIGatewayResponse.to_response({"classroom": classroom.to_dict()})


def create_classmate_invite_link_handler(event, context):
    path = event["pathParameters"]
    classroom_id = ClassroomId(int(path["classroom_id"]))
    user_id = AuthenticationEventPerser.parse(event)
    logger = getLogger()
    service: CreateClassmateInviteLink = create_classmate_invite_link(
        logger=logger)
    classmate_invite = service.run(user_id, classroom_id)
    return APIGatewayResponse.to_response(
        {"classmate_invite": classmate_invite.to_dict()})


def request_join_classroom_handler(event, context):
    path = event["pathParameters"]
    classroom_id = ClassroomId(int(path["classroom_id"]))
    user_id = AuthenticationEventPerser.parse(event)
    logger = getLogger()
    service: RequestJoinClassroom = request_join_classroom(logger=logger)
    classmate = service.run(user_id, classroom_id)
    return APIGatewayResponse.to_response({"classmate": classmate.to_dict()})


def approve_join_classroom_request_handler(event, context):
    user_id = AuthenticationEventPerser.parse(event)
    logger = getLogger()
    path = event["pathParameters"]
    classroom_id = ClassroomId(int(path["classroom_id"]))
    data = json.loads(event["body"])
    approve_user_list = data.get('approve_user_list')
    if not approve_user_list:
        raise Exception('accept_user_list is required.')

    service: ApproveJoinClassroomRequest = approve_join_classroom_request(
        logger=logger)
    service.run(user_id, classroom_id, [UserId(d) for d in approve_user_list])
    return APIGatewayResponse.to_response({})


def get_my_classroom_list_handler(event, context):
    user_id = AuthenticationEventPerser.parse(event)
    logger = getLogger()
    service: MyClassroomList = get_my_classroom_list(logger=logger)
    classroom_list = service.run(user_id)
    return APIGatewayResponse.to_response(
        {"my_classroom_list": classroom_list.to_list()})
