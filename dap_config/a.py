from dap_common.api_logger import api_log


class a:
    def __init__(self):
        self.log = api_log()

    def log_info(self):
        self.log.info('333333333333333')


if __name__ == '__main__':
    bb = a()
    bb.log_info()
