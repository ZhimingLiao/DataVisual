# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州富力海珠城3810  志明  2019-09-17 15:40
# 当前计算机登录名称 :andy
# 项目名称  :DataVisual
# 编译器   :PyCharm

__author____ = 'Andy Liao'
__time__ = '2019-09-17 15:40'

if __name__ == '__main__':
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(os.path.join(os.path.dirname(BASE_DIR), "static"))
