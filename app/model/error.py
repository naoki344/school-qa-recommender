from logging import ERROR
from logging import WARNING


class LogLevel:
    pass


class ClientError(Exception):
    level = WARNING
    status_code = 400


class ServerError(Exception):
    level = ERROR
    status_code = 500


class UserAlreadyRegisteredInThisClassroom(ClientError):
    pass


class OnlyTheOwnerCanCreate(ClientError):
    pass


class OnlyTheOwnerCanUpdate(ClientError):
    pass
