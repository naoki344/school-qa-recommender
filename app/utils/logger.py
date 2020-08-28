from logging import Logger


class CWLogger(Logger):
    def __init__(self, context, log_level):
        self.function_name = context.function_name
        self.error_log_group_name = '/aws/lambda/devmiyoshi-tt-error-log'
        super().__init__(self, context.function_name, self.log_level)

    def exception(self, msg, *args, **kwargs):
        msg = makeLogRecord()
        pass


def getCWLogger(context, log_level: str = "INFO"):
    return CWLogger(context, log_level)
