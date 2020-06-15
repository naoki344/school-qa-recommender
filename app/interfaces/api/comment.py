import json
from logging import getLogger

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.application.usecase.comment import GetWorkCommentList
from app.application.usecase.comment import RegisterWorkComment
from app.configure.usecase.comment import get_work_comment_list
from app.configure.usecase.comment import register_work_comment
from app.interfaces.api.response import APIGatewayErrorResponse
from app.interfaces.api.response import APIGatewayResponse
from app.model.classroom.classroom import ClassroomId
from app.model.work.work import WorkId


def register_work_comment_handler(event, context):
    try:
        logger = getLogger()
        path = event["pathParameters"]
        classroom_id = ClassroomId(int(path["classroom_id"]))
        work_id = WorkId(int(path["work_id"]))
        data = json.loads(event["body"])
        service: RegisterWorkComment = \
            register_work_comment(logger=logger)
        user_id = AuthenticationEventPerser.parse(event)
        comment = service.run(user_id,
                              classroom_id=classroom_id,
                              work_id=work_id,
                              data=data)
        return APIGatewayResponse.to_response({"comment": comment.to_dict()})
    except Exception as e:
        logger.exception(e)
        return APIGatewayErrorResponse.to_response(e)


def get_work_comment_list_handler(event, context):
    try:
        logger = getLogger()
        path = event["pathParameters"]
        classroom_id = ClassroomId(int(path["classroom_id"]))
        work_id = ClassroomId(int(path["work_id"]))
        service: GetWorkCommentList = \
            get_work_comment_list(logger=logger)
        user_id = AuthenticationEventPerser.parse(event)
        work_comment_list = service.run(user_id,
                                        classroom_id=classroom_id,
                                        work_id=work_id)
        return APIGatewayResponse.to_response(work_comment_list.to_response())
    except Exception as e:
        logger.exception(e)
        return APIGatewayErrorResponse.to_response(e)
