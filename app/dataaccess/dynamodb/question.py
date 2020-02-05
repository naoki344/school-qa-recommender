from logging import Logger

from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.dataaccess.aws.dynamodb import DynamoDBClient


class QuestionDatasource:
    def __init__(self, client: DynamoDBClient, logger: Logger) -> None:
        self.client = client
        self.logger = logger

    def insert_item(self, item: Question) -> None:
        self.client.put_item(item.to_dict())

    def find_by_id(self, question_id: QuestionId) -> Question:
        data = self.client.get_item(
            {'question_id': question_id.value})
        return Question.from_dict(data)
