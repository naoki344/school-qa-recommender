from logging import Logger
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.dataaccess.dynamodb.question import QuestionDatasource


class CreateQuestion:
    def __init__(self, question_datasource: QuestionDatasource,
                 logger: Logger) -> None:
        self.datasource = question_datasource

    def run(self, item: dict) -> Question:
        question_id = self.datasource.fetch_sequesnse_id()
        question = Question.create(question_id, item)
        # TODO: validation
        self.datasource.insert_item(question)
        return question


class UpdateQuestion:
    def __init__(self, question_datasource: QuestionDatasource,
                 logger: Logger) -> Question:
        self.datasource = question_datasource

    def run(self, question_id: QuestionId, item: dict) -> None:
        question = Question.from_dict(item)
        if question_id != question.question_id:
            raise Exception("更新するItemとKeyのIDが一致していません")
        self.datasource.put_item(question)
        return question


class FindQuestion:
    def __init__(self, question_datasource: QuestionDatasource,
                 logger: Logger) -> Question:
        self.datasource = question_datasource

    def run(self, question_id: QuestionId) -> Question:
        return self.datasource.find_by_id(question_id)
