from logging import Logger
from typing import List
from typing import Optional
from typing import Union

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.dynamodb.sequences import SequensesDatasource
from app.model.question.question import Question
from app.model.question.question import QuestionCard
from app.model.question.question import QuestionId
from app.model.question.question import RegisterUserId


class QuestionDatasource:
    def __init__(self, client: DynamoDBClient,
                 sequenses_table: SequensesDatasource, logger: Logger) -> None:
        self.client = client
        self.sequenses_table = sequenses_table
        self.logger = logger

    def insert_item(self, item: Question) -> None:
        self.client.insert_item(item.to_dict(), "question_id")

    def put_item(self, item: Question) -> None:
        self.client.put_item(item.to_dict())

    def fetch_sequense_id(self) -> int:
        name = f"Dynamodb#{self.client.table.table_name}"
        _id = self.sequenses_table.fetch_sequense_id(name)
        return _id

    def find_by_id(self, question_id: QuestionId) -> Question:
        data = self.client.get_item({'question_id': question_id.value})
        if data:
            return Question.from_dict(data)
        raise Exception(f'Question not found. {question_id: {question_id}}')

    def get_register_user_index(
        self, register_user_id: RegisterUserId
    ) -> Union[List[QuestionCard], Optional[str]]:
        names = {'#user_id': 'register_user_id'}
        values = {':value': register_user_id.value}
        expression = '#user_id = :value'
        data, paging_key = self.client.query(index_name='RegisterUserId-Index',
                                             names=names,
                                             values=values,
                                             expression=expression)
        _list = []
        for d in data:
            try:
                _list.append(QuestionCard.from_db(d))
            except Exception as e:
                self.logger.error(e)
        return _list, paging_key
