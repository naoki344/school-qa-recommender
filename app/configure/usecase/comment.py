from logging import Logger

from app.application.usecase.comment import GetWorkCommentList
from app.application.usecase.comment import RegisterWorkComment
from app.application.usecase.comment import ModifyWorkComment
from app.configure.query.classroom import classroom_query_service
from app.configure.query.user import user_query_service
from app.configure.query.work import work_query_service
from app.configure.resoruce.dynamodb import work_comment_datasource


def register_work_comment(logger: Logger) -> RegisterWorkComment:
    datasource = work_comment_datasource(logger)
    work_service = work_query_service(logger)
    user_service = user_query_service(logger)
    classroom_service = classroom_query_service(logger)
    return RegisterWorkComment(comment_datasource=datasource,
                               work_service=work_service,
                               classroom_service=classroom_service,
                               user_service=user_service,
                               logger=logger)


def modify_work_comment(logger: Logger) -> ModifyWorkComment:
    datasource = work_comment_datasource(logger)
    user_service = user_query_service(logger)
    return ModifyWorkComment(comment_datasource=datasource,
                             user_service=user_service,
                             logger=logger)


def get_work_comment_list(logger: Logger) -> RegisterWorkComment:
    datasource = work_comment_datasource(logger)
    work_service = work_query_service(logger)
    user_service = user_query_service(logger)
    classroom_service = classroom_query_service(logger)
    return GetWorkCommentList(comment_datasource=datasource,
                              work_service=work_service,
                              classroom_service=classroom_service,
                              user_service=user_service,
                              logger=logger)
