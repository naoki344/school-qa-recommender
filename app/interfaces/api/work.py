import json
from logging import getLogger

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.application.usecase.work import CreateWorkFromQuestion
from app.application.usecase.work import GetClassroomWorkList
from app.configure.usecase.work import create_work_from_question
from app.configure.usecase.work import get_classroom_work_list
from app.interfaces.api.response import APIGatewayResponse
from app.model.classroom.classroom import ClassroomId
from app.model.question.question import QuestionId


def create_work_from_question_handler(event, context):
    path = event["pathParameters"]
    classroom_id = ClassroomId(int(path["classroom_id"]))
    question_id = QuestionId(int(path["question_id"]))
    data = json.loads(event["body"])
    service: CreateWorkFromQuestion = \
        create_work_from_question(logger=getLogger())
    user_id = AuthenticationEventPerser.parse(event)
    work = service.run(user_id,
                       question_id=question_id,
                       classroom_id=classroom_id,
                       data=data)
    return APIGatewayResponse.to_response({"work": work.to_dict()})


def get_classroom_work_list_handler(event, context):
    path = event["pathParameters"]
    classroom_id = ClassroomId(int(path["classroom_id"]))
    service: GetClassroomWorkList = \
        get_classroom_work_list(logger=getLogger())
    user_id = AuthenticationEventPerser.parse(event)
    work_list = service.run(user_id=user_id, classroom_id=classroom_id)
    return APIGatewayResponse.to_response(
        {"work_list": [work.to_dict() for work in work_list]})
