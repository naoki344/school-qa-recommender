from logging import Logger
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.dataaccess.dynamodb.question import QuestionDatasource


class CreateQuestion:
    def __init__(self, question_datasource: QuestionDatasource,
                 logger: Logger) -> None:
        self.datasource = question_datasource

    def run(self, item: Question) -> None:
        self.datasource.insert_item(item)


class FindQuestion:
    def __init__(self, question_datasource: QuestionDatasource,
                 logger: Logger) -> None:
        self.datasource = question_datasource

    def run(self, question_id: QuestionId) -> Question:
        return self.datasource.find_by_id(question_id)
