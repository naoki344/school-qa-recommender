from logging import Logger

from app.application.query.work import WorkQueryService
from app.configure.resoruce.dynamodb import work_datasource


def work_query_service(logger: Logger) -> WorkQueryService:
    datasource = work_datasource(logger=logger)
    return WorkQueryService(work_datasource=datasource, logger=logger)
