# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-05-22 11:07
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-22 11:07'


class Singleton:
    __cls = dict()

    def __init__(self, cls):
        self.__key = cls

    # 在 初始化方法之后调用
    def __call__(self, *args, **kwargs):
        if self.__key not in self.__cls:
            self[self.__key] = self.__key(*args, **kwargs)
        return self[self.__key]

    def __setitem__(self, key, value):
        self.__cls[key] = value

    def __getitem__(self, item):
        return self.__cls[item]


if __name__ == '__main__':
    print("test")
