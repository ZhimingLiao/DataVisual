# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州  志明  2019-06-03 8:48
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-06-03 8:48'

import socket


# 1.检测指定ip的端口是否可用
def test_port(ip='192.168.6.71', port=3300):
    '''
    检测指定的IP的端口是否开启监听
    :param ip: 测试ip地址
    :param port: 连接的端口号
    :return: 处理结果
    '''
    # 使用TCP连接方式
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        st.settimeout(2)
        st.connect((ip, port))
        # print("%s的IP的端口%d已连接!" % (ip, port))
    except WindowsError:
        result = False
        error = 1
    except Exception:
        result = False
        error = 2
    else:
        result = True
        error = 0
    finally:
        st.close()
        return {'error': error, 'msg': f'ip:{ip};端口号{port}连接成功' if error < 1 else f'ip:{ip};端口号{port}未开放',
                'result': result}


# 2.创建TCP套接字对象
def test_tcp_create(ip='192.168.111.176', port=3600):
    if test_port(ip=ip, port=port).get('error') > 0:
        return {'error': 3, 'msg': '远程ip或端口积极拒绝访问'}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return {'error': 0, 'msg': '套接字对象创建成功!', 'data': sock}


# 3.使用socket对象进行发送数据
def test_tcp_send(sock=None, datas=None, start='\x0b', end='\x1c\x0d', encode='utf8'):
    """
    使用指定的套接字对象发送字节码数据;适用于已经创建的套接字,原型来自于hl7消息测试
    :param sock: 套接字对象
    :param datas: 二进制数据
    :param start: 开始标识符
    :param end: 结束标识符
    :param encode: 数据编码
    :return: 返回字典数据
    """
    # 1. 对入参进行过滤处理
    if not sock:
        return {'error': 1, 'msg': '套接字对象Socket未提供!'}
    # 1.组装数据,添加尾部和头部
    datas_zip = start.encode() + datas.encode() + end.encode()
    # 2. 发送数据到指定ip和端口
    sock.send(datas_zip)
    data = ''
    # 循环接受套接字数据
    while True:
        print(f'正在接收中...')
        rec = sock.recv(1024)
        print(f'已接受到数据:\n{rec}')
        data = data + rec.decode(encode)
        if rec.find('\x1c\x0d'.encode()) != -1:
            print('数据接收结束,退出!')
            break
        else:
            continue
        # print(data)
    # print(t[t.find(b'\x0b')+1:t.find(b'\x1c')])
    sock.close()
    # 去除消息内容尾部
    data = data.rstrip('\x1c\x0d')
    return {'error': 0, 'msg': '成功接受到数据!', 'data': data}


# 4.发送数据
def send_data():
    from test_timer import Timer
    ip_test = '127.0.0.1'
    port_test = 20000
    msg = 'MSH|^~\\&|LIS||NHIS||20190528085648||OUL^R21|793867|P|2.4|||AL|AL\r' \
          + 'PID|||^^^^IDCard~^^^^IdentifyNO~^^^^Outpatient~201940226^^^^PatientNO||朱子涵|||F\r' \
          + 'PV1||I|^^^696^儿1科||||||0545^朱晓虎||||||||||201940226|||||||||||||||||||||||||20190522100642\r' \
          + 'OBR|1|1005450034391|119052258274|06671^血培养(加药敏进口仪器）^MIC||20190522113802|||||||||0002&' \
            '静脉全血|||儿1科|696|||20190528085648||||||||||0729|0209\r' \
          + 'NTE|1\r' \
          + 'OBX|14140288|TX|^^^05051104^培养7天无细菌生长||||||||F|||20190528085648\r'

    with Timer.time_cost():
        st = test_tcp_create(ip_test, port_test)
        if st.get('error') > 0:
            print(st.get('msg'))
            exit(1)
        else:
            st = st.get('data')
            result = test_tcp_send(sock=st, datas=msg)
            from demo.loger.Logger import Logger
            Logger("DEBUG", use_console=True, log_path=r'D:\log').info(result['data'])


if __name__ == '__main__':
    print(send_data())
