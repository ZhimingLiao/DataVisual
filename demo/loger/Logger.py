# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-05-22 10:29
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-22 10:29'

'''
该日志类可以把不同级别的日志输出到不同的日志文件中
'''
import logging
import os
import sys
import time

from .Singleton import Singleton


@Singleton
class Logger:
    def __init__(self, set_level="INFO", filename=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y-%m-%d.log", time.localtime()),
                 log_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"),
                 use_console=True):
        """
        :param set_level: 日志级别["NOTSET"|"DEBUG"|"INFO"|"WARNING"|"ERROR"|"CRITICAL"]，默认为INFO
        :param name: 日志中打印的name，默认为运行程序的name
        :param log_name: 日志文件的名字，默认为当前时间（年-月-日.log）
        :param log_path: 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
        :param use_console: 是否在控制台打印，默认为True
        """
        if not set_level:
            # 设置set_level为None，自动获取当前运行模式
            set_level = self._exec_type()

        self.__logger = logging.getLogger(filename)
        # 1,设置日志等级
        self.setLevel(getattr(logging, set_level.upper()) if hasattr(logging, set_level.upper()) else logging.INFO)
        # 创建日志目录
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # 2,设置日志打印格式
        formats = '1.日志时间:%(asctime)s;日志级别:%(levelno)s;日志级别名称:%(levelname)s;\n' \
                  '2.模块名称:%(filename)s;函数名称:%(funcName)s;日志打印行号:%(lineno)d;模块完整路径:%(pathname)s;\n' \
                  '3.线程ID:%(thread)d;线程名字:%(threadName)s;进程ID:%(process)d;\n' \
                  '4.日志信息内容:%(message)s;\n' + '-' * 80
        formatter = logging.Formatter(formats)
        # 日志处理集合
        handler_list = list()
        # 文件流
        handler_list.append(logging.FileHandler(os.path.join(log_path, log_name), encoding="utf-8"))
        if use_console:
            handler_list.append(logging.StreamHandler())
        for handler in handler_list:
            handler.setFormatter(formatter)
            self.addHandler(handler)

    @staticmethod
    def _exec_type():
        return "DEBUG" if os.environ.get("PYTHONENABLE") else "INFO"

    def __getattr__(self, item):
        return getattr(self.logger, item)

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, func):
        self.__logger = func


if __name__ == '__main__':
    logger = Logger("DEBUG", use_console=True).warning("调试")
