from logging import Logger

from app.dataaccess.dynamodb.work import WorkDatasource
from app.model.work.work import Work
from app.model.work.work import WorkId


class WorkQueryService:
    def __init__(self, work_datasource: WorkDatasource,
                 logger: Logger) -> None:
        self.work_datasource = work_datasource
        self.logger = logger

    def find(self, work_id: WorkId) -> Work:
        return self.work_datasource.find_by_id(work_id)
