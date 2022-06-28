import json
from logging import getLogger

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.application.usecase.work import CreateWorkFromQuestion
from app.application.usecase.work import FindClassroomWork
from app.application.usecase.work import GetClassroomWorkList
from app.configure.usecase.work import create_work_from_question
from app.configure.usecase.work import find_classroom_work
from app.configure.usecase.work import get_classroom_work_list
from app.interfaces.api.response import APIGatewayErrorResponse
from app.interfaces.api.response import APIGatewayResponse
from app.model.classroom.classroom import ClassroomId
from app.model.work.work import WorkId


def create_work_from_question_handler(event, context):
    try:
        logger = getLogger()
        path = event["pathParameters"]
        classroom_id = ClassroomId(int(path["classroom_id"]))
        data = json.loads(event["body"])
        service: CreateWorkFromQuestion = \
            create_work_from_question(logger=logger)
        user_id = AuthenticationEventPerser.parse(event)
        work = service.run(user_id, classroom_id=classroom_id, data=data)
        return APIGatewayResponse.to_response({"work": work.to_dict()})
    except Exception as e:
        logger.exception(e)
        return APIGatewayErrorResponse.to_response(e)


def get_classroom_work_list_handler(event, context):
    try:
        logger = getLogger()
        path = event["pathParameters"]
        classroom_id = ClassroomId(int(path["classroom_id"]))
        service: GetClassroomWorkList = \
            get_classroom_work_list(logger=logger)
        user_id = AuthenticationEventPerser.parse(event)
        work_list = service.run(user_id=user_id, classroom_id=classroom_id)
        return APIGatewayResponse.to_response(
            {"work_list": [work.to_dict() for work in work_list]})
    except Exception as e:
        logger.exception(e)
        return APIGatewayErrorResponse.to_response(e)


def find_classroom_work_handler(event, context):
    try:
        logger = getLogger()
        path = event["pathParameters"]
        classroom_id = ClassroomId(int(path["classroom_id"]))
        work_id = WorkId(int(path["work_id"]))
        service: FindClassroomWork = \
            find_classroom_work(logger=logger)
        user_id = AuthenticationEventPerser.parse(event)
        work, question, comment_list = service.run(user_id=user_id,
                                                   classroom_id=classroom_id,
                                                   work_id=work_id)
        return APIGatewayResponse.to_response({
            "work": work.to_dict(),
            "question": question.to_dict(),
            "comment_list": comment_list
        })
    except Exception as e:
        logger.exception(e)
        return APIGatewayErrorResponse.to_response(e)
