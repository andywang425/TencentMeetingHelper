import logging
import colorlog
import os
from datetime import datetime


class Log:
    def __init__(self, name=None, log_level=logging.DEBUG, save2file=False, path=''):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        # 日志格化字符串
        console_fmt = '%(asctime)s %(levelname)s: %(log_color)s%(message)s'
        file_fmt = '%(asctime)s [%(levelname)s]: %(message)s'
        # 时间格式化字符串
        console_date_fmt = '%Y-%m-%d %H:%M:%S'
        file_date_fmt = '%H:%M:%S'
        # 控制台输出不同级别日志颜色设置
        color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple',
        }
        console_formatter = colorlog.ColoredFormatter(
            fmt=console_fmt, datefmt=console_date_fmt, log_colors=color_config)
        # 输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        # 输出到文件
        if (save2file):
            file_formatter = logging.Formatter(fmt=file_fmt, datefmt=file_date_fmt)
            newPath = path.replace('{DATE}', datetime.now().strftime('%Y-%M-%d'))
            dir = os.path.dirname(newPath)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file_handler = logging.FileHandler(filename=newPath,  encoding='utf-8')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

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
