import logging
import colorlog


class Log:
    def __init__(self, name=None, log_level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        # 日志格化字符串
        console_fmt = '%(asctime)s %(levelname)s: %(log_color)s%(message)s'
        # 时间格式化字符串
        date_fmt = '%Y-%m-%d %H:%M:%S'
        # 控制台输出不同级别日志颜色设置
        color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple',
        }
        console_formatter = colorlog.ColoredFormatter(fmt=console_fmt, datefmt=date_fmt, log_colors=color_config)
        # 输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
