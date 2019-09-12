# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州  志明  2019-06-03 9:06
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-06-03 9:06'

import logging
from contextlib import contextmanager

from time import perf_counter


class Timer(object):
    name = '计时器(默认)'

    def __init__(self, name='计时器(默认)') -> None:
        super().__init__()
        Timer.name = name

    # 1，统计语句执行所花费时间
    @staticmethod
    @contextmanager
    def time_cost():
        try:
            start = perf_counter()
            yield
        finally:
            end = perf_counter()
            logging.basicConfig(level=logging.DEBUG, format='%(message)s')
            logging.debug(msg=f'根据统计共花费时间为:{end - start}秒')


if __name__ == '__main__':
    with Timer.time_cost():
        for _ in range(10000):
            print("test")
