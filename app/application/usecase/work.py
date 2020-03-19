from logging import Logger
from typing import List

from app.application.query.classroom import ClassroomQueryService
from app.application.query.question import QuestionQueryService
from app.application.query.user import UserQueryService
from app.dataaccess.dynamodb.work import WorkDatasource
from app.model.classroom.classroom import ClassroomId
from app.model.question.question import QuestionId
from app.model.user.user import UserId
from app.model.work.work import Work


class CreateWorkFromQuestion:
    def __init__(self, work_datasource: WorkDatasource,
                 question_serice: QuestionQueryService,
                 classroom_serice: ClassroomQueryService,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.work_datasource = work_datasource
        self.question_serice = question_serice
        self.classroom_serice = classroom_serice
        self.user_service = user_service
        self.logger = logger

    def run(self, user_id: UserId, question_id: QuestionId,
            classroom_id: ClassroomId, data: dict):
        user = self.user_service.find(user_id)
        question = self.question_serice.find(question_id)
        classroom = self.classroom_serice.find(classroom_id)
        _id = self.work_datasource.fetch_sequense_id()
        work = Work.create_from_question(_id, classroom.classroom_id, user,
                                         question, data)
        self.work_datasource.insert_item(work)
        return work


class GetClassroomWorkList:
    def __init__(self, work_datasource: WorkDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.work_datasource = work_datasource
        self.user_service = user_service
        self.logger = logger

    def run(self, user_id: UserId, classroom_id: ClassroomId) -> List[Work]:
        _ = self.user_service.find(user_id)
        work_list = self.work_datasource.find_by_classroom_id(classroom_id)
        return work_list
