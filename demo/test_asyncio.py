# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州富力海珠城3810  志明  2019-09-08 9:02
# 当前计算机登录名称 :andy
# 项目名称  :DataVisual
# 编译器   :PyCharm
import asyncio as asy
import random
import socket
import threading

__author____ = 'Andy Liao'
__time__ = '2019-09-08 9:02'


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
    except Exception as e:
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
    '''
    使用指定的套接字对象发送字节码数据;适用于已经创建的套接字,原型来自于hl7消息测试
    :param sock: 套接字对象
    :param datas: 二进制数据
    :param start: 开始标识符
    :param end: 结束标识符
    :return:
    '''
    thread = threading.current_thread()
    print(f'当前线程:{thread.getName(), thread.ident}')
    # 1. 对入参进行过滤处理
    if not sock:
        return {'error': 1, 'msg': '套接字对象Socket未提供!'}

    # 2. 发送数据到指定ip和端口
    sock.send((start + datas + end).encode(encode))
    data = ''
    # 循环接受套接字数据
    while True:
        print(f'正在接收中...')
        rec = sock.recv(1024)
        # print(f'已接受到数据:\n{rec}')
        data = data + rec.decode()
        if rec.find('\x0d'.encode()) != -1:
            print('数据接收结束,退出!')
            break
        else:
            continue
        # print(data)
    # print(t[t.find(b'\x0b')+1:t.find(b'\x1c')])
    # 去除消息内容尾部
    data = data.rstrip('\x0d')
    return {'error': 0, 'msg': '成功接受到数据!', 'data': data}


def test1():
    from test_timer import Timer
    with Timer.time_cost():
        ip_test = '127.0.0.1'
        port_test = 5000
        msg = r'MSH|^~\&|LIS||NHIS||20190528085648||OUL^R21|793867|P|2.4|||AL|AL\r' \
              + r'PID|||^^^^IDCard~^^^^IdentifyNO~^^^^Outpatient~201940226^^^^PatientNO||朱子涵|||F\r' \
              + r'PV1||I|^^^696^儿1科||||||0545^朱晓虎||||||||||201940226|||||||||||||||||||||||||20190522100642\r' \
              + r'OBR|1|1005450034391|119052258274|06671^血培养(加药敏进口仪器）^MIC||20190522113802|||||||||0002&' \
                r'静脉全血|||儿1科|696|||20190528085648||||||||||0729|0209\r' \
              + r'NTE|1\r' \
              + r'OBX|14140288|TX|^^^05051104^培养7天无细菌生长||||||||F|||20190528085648\r'
        st = test_tcp_create(ip_test, port_test)
        if st.get('error') > 0:
            print(st.get('msg'))
            exit(1)
        else:
            st = st.get('data')
        loop = asy.get_event_loop()
        # gat = asy.gather(test_tcp_send(sock=st, datas=msg) for i in range(100))
        # task = [test_tcp_send(sock=st, datas=msg) for i in range(100)]
        # loop.run_until_complete(asy.wait(task))
        loop.run_until_complete(asy.gather(*[test_tcp_send(sock=st, datas=msg) for i in range(100)]))
        st.close()


def test2():
    thread = threading.current_thread()
    print(f'当前线程:{thread.getName(), thread.ident}')
    ip_test = '127.0.0.1'
    port_test = 5000
    msg = r'MSH|^~\&|LIS||NHIS||20190528085648||OUL^R21|793867|P|2.4|||AL|AL\r' \
          + r'PID|||^^^^IDCard~^^^^IdentifyNO~^^^^Outpatient~201940226^^^^PatientNO||朱子涵|||F\r' \
          + r'PV1||I|^^^696^儿1科||||||0545^朱晓虎||||||||||201940226|||||||||||||||||||||||||20190522100642\r' \
          + r'OBR|1|1005450034391|119052258274|06671^血培养(加药敏进口仪器）^MIC||20190522113802|||||||||0002&' \
            r'静脉全血|||儿1科|696|||20190528085648||||||||||0729|0209\r' \
          + r'NTE|1\r' \
          + r'OBX|14140288|TX|^^^05051104^培养7天无细菌生长||||||||F|||20190528085648\r'

    st = test_tcp_create(ip_test, port_test)
    if st.get('error') > 0:
        print(st.get('msg'))
        exit(1)
    else:
        st = st.get('data')
        result = test_tcp_send(sock=st, datas=msg)
        from demo.loger.Logger import Logger
        Logger("DEBUG", use_console=True).info(result['data'])


def test3():
    t = random.random()
    print(t)


def test4():
    import time
    start = time.time()
    from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
    # 创建包含2个线程的线程池
    with ThreadPoolExecutor(max_workers=3) as executor:
        '''map_fun：你传入的要执行的map函数
           itr_arg：一个可迭代的参数，可以是列表字典等可迭代的对象
           基本上和python的map函数一样
           注意result并不是你map_fun返回的结果，而是一个生成器，如果要从中去结果，你可以使用列表生成式或者其他你想使用的方法
        '''
        task = [executor.submit(test2) for _ in range(100)]
        wait(fs=task, timeout=2, return_when=ALL_COMPLETED)

        print('finished')
    print(f'共花费时间:{time.time() - start}毫秒')


if __name__ == '__main__':
    # 测试代码执行效率
    # import timeit
    # ti = timeit.repeat(stmt=test2, setup='', number=10, repeat=2)
    # print(ti)
    test4()
