# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州富力海珠城3810  志明  2019-08-29 16:13
# 当前计算机登录名称 :andy
# 项目名称  :DataVisual
# 编译器   :PyCharm

__author____ = "Andy Liao"
__time__ = "2019-08-29 16:13"
import cx_Oracle


def read_db(data):
    ip, port, SID = "192.168.50.40", 1521, "orcl"
    try:
        dsn_tns = cx_Oracle.makedsn(ip, port, SID)
        conn = cx_Oracle.connect("zm_test", "zm_test", dsn_tns)
    except cx_Oracle.DatabaseError as e:
        return {"error": 1, "msg": "数据库连接错误"}
    except Exception as e:
        # return {'error': -1, 'msg': '未知错误'}
        raise e
    else:
        cur = conn.cursor()
        sql = ""
        for index in range(len(data)):
            print(data[index])
            sql = (
                    "insert into DIC_NATIONALITY(code, name, name_en) values ('"
                    + data[index][0]
                    + "','"
                    + data[index][1]
                    + "','"
                    + data[index][2]
                    + "')"
            )
            cur.execute(sql)
        conn.commit()
        cur.close()
        return {"error": 0, "msg": "处理成功!", "result": sum}


if __name__ == "__main__":
    file_path = "demo.txt"
    data = list()
    with open(file_path, encoding="utf8", newline="", mode="r") as f:
        tmp = f.readline()
        while tmp != "":
            data.append(tmp.replace("\r\n", "").replace(",", ""))
            tmp = f.readline()
    import re

    t = list()
    data2 = list()
    for i in range(len(data)):
        try:
            index = data[i].index(re.search(r"\d+", data[i]).group())
            index2 = data[i][index::].split(" ")
        except AttributeError as e:
            # print(data[i], e)
            continue
        else:
            # print(data[i], data[i][index-3: index], index2[0][3::])
            # data2[data[i][index-3: index]] = index2[0][3::]
            t.append(data[i][index - 3: index])
            t.append(index2[0][3::])
            t.append((" ".join(index2[1::])).replace("'", "&"))
            data2.append(t)
            del t
            t = list()
    print(read_db(data2))
