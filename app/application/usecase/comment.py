from logging import Logger

from app.application.query.classroom import ClassroomQueryService
from app.application.query.user import UserQueryService
from app.application.query.work import WorkQueryService
from app.dataaccess.dynamodb.comment import WorkCommentDatasource
from app.model.classroom.classroom import ClassroomId
from app.model.comment.comment import WorkComment
from app.model.comment.comment import WorkCommentList
from app.model.user.user import UserId
from app.model.work.work import WorkId


class RegisterWorkComment:
    def __init__(self, comment_datasource: WorkCommentDatasource,
                 work_service: WorkQueryService,
                 classroom_service: ClassroomQueryService,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.comment_datasource = comment_datasource
        self.work_service = work_service
        self.classroom_service = classroom_service
        self.user_service = user_service
        self.logger = logger

    def run(self, user_id: UserId, classroom_id: ClassroomId, work_id: WorkId,
            data: dict) -> WorkComment:
        user = self.user_service.find(user_id)
        # TODO: Classmateかどうかのチェック
        work = self.work_service.find(work_id)
        if work.classroom_id != classroom_id:
            raise Exception('Resource not found')
        _id = self.comment_datasource.fetch_sequense_id()
        comment = WorkComment.create(work_id, user, _id,
                                     data.get("comment_type"),
                                     data.get("parent_comment_id"),
                                     data["body"])
        self.comment_datasource.insert_item(comment)
        return comment


class GetWorkCommentList:
    def __init__(self, comment_datasource: WorkCommentDatasource,
                 work_service: WorkQueryService,
                 classroom_service: ClassroomQueryService,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.comment_datasource = comment_datasource
        self.work_service = work_service
        self.classroom_service = classroom_service
        self.user_service = user_service
        self.logger = logger

    def run(self, user_id: UserId, classroom_id: ClassroomId,
            work_id: WorkId) -> WorkCommentList:
        _ = self.user_service.find(user_id)
        # TODO: Classmateかどうかのチェック
        work = self.work_service.find(work_id)
        if work.classroom_id != classroom_id:
            raise Exception('Resource not found')
        work_comment_list = self.comment_datasource.find_by_work_id(work_id)
        return work_comment_list
