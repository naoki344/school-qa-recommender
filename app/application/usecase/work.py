from logging import Logger
from typing import List

from app.application.query.classroom import ClassroomQueryService
from app.application.query.question import QuestionQueryService
from app.application.query.user import UserQueryService
from app.dataaccess.dynamodb.comment import WorkCommentDatasource
from app.dataaccess.dynamodb.work import WorkDatasource
from app.model.classroom.classroom import ClassroomId
from app.model.comment.comment import WorkComment
from app.model.question.question import QuestionId
from app.model.user.user import UserId
from app.model.work.work import OriginType
from app.model.work.work import Work
from app.model.work.work import WorkId


class CreateWorkFromQuestion:
    def __init__(self, work_datasource: WorkDatasource,
                 comment_datasource: WorkCommentDatasource,
                 question_service: QuestionQueryService,
                 classroom_service: ClassroomQueryService,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.work_datasource = work_datasource
        self.question_service = question_service
        self.classroom_service = classroom_service
        self.comment_datasource = comment_datasource
        self.user_service = user_service
        self.logger = logger

    def run(self, user_id: UserId, classroom_id: ClassroomId, data: dict):
        user = self.user_service.find(user_id)
        question = self.question_service.find(
            QuestionId(int(data["question_id"])))
        classroom = self.classroom_service.find(classroom_id)
        _id = self.work_datasource.fetch_sequense_id()
        work = Work.create_from_question(_id, classroom.classroom_id, user,
                                         question, data)
        self.work_datasource.insert_item(work)

        _comment_id = self.comment_datasource.fetch_sequense_id()
        comment = WorkComment.create_main_topic(work.work_id, user,
                                                _comment_id)
        self.comment_datasource.insert_item(comment)
        return work


class GetClassroomWorkList:
    def __init__(self, work_datasource: WorkDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.work_datasource = work_datasource
        self.user_service = user_service
        self.logger = logger

    def run(self, user_id: UserId, classroom_id: ClassroomId) -> List[Work]:
        _ = self.user_service.find(user_id)
        # TODO: Classmateかどうかのチェック
        work_list = self.work_datasource.find_by_classroom_id(classroom_id)
        return work_list


class FindClassroomWork:
    def __init__(self, work_datasource: WorkDatasource,
                 question_service: QuestionQueryService,
                 classroom_service: ClassroomQueryService,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.work_datasource = work_datasource
        self.question_service = question_service
        self.classroom_service = classroom_service
        self.user_service = user_service
        self.logger = logger

    def run(self, user_id: UserId, classroom_id: ClassroomId,
            work_id: WorkId) -> List[Work]:
        _ = self.user_service.find(user_id)
        # TODO: Classmateかどうかのチェック
        work = self.work_datasource.find_by_id(work_id)
        comment_list = []
        if work.origin_type is OriginType.question:
            question = self.question_service.find(
                QuestionId(work.origin_id.value))
            return work, question, comment_list,
        return work, None, comment_list,
