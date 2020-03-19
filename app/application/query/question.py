from logging import Logger
from typing import List
from typing import Optional
from typing import Union

from app.dataaccess.dynamodb.question import QuestionDatasource
from app.model.question.question import Question
from app.model.question.question import QuestionCard
from app.model.question.question import QuestionId
from app.model.question.question import RegisterUserId


class QuestionQueryService:
    def __init__(self, question_datasource: QuestionDatasource,
                 logger: Logger) -> Question:
        self.datasource = question_datasource
        self.logger = logger

    def find(self, question_id: QuestionId) -> Question:
        return self.datasource.find_by_id(question_id)

    def find_by_user_id(
        self,
        register_user_id: Optional[RegisterUserId] = None
    ) -> Union[List[QuestionCard], Optional[str]]:
        return self.datasource.get_register_user_index(register_user_id)
