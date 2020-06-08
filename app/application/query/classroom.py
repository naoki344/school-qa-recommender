from logging import Logger
from typing import Tuple

from app.dataaccess.dynamodb.classroom import ClassroomDatasource
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId


class ClassroomQueryService:
    def __init__(self, datasource: ClassroomDatasource,
                 logger: Logger) -> Classroom:
        self.datasource = datasource

    def find(self, classroom_id: ClassroomId) -> Classroom:
        return self.datasource.find_by_id(classroom_id)
