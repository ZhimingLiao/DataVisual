# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州富力海珠城3810  志明  2019-09-11 8:17
# 当前计算机登录名称 :andy
# 项目名称  :DataVisual
# 编译器   :PyCharm

__author____ = 'Andy Liao'
__time__ = '2019-09-11 8:17'
# 生成数字摘要,数字签名使用
import hashlib
import random

# 产生rsa公钥和密钥对,需要pip install rsa,非内置模块
# 使用对称密码进行加密,非内置需要安装
from Crypto.Cipher import AES, PKCS1_OAEP as pk
from Crypto.PublicKey import RSA


# 1.md5数字摘要签名
def get_md5(data=None, encoding="utf8"):
    if data and isinstance(data, (str,)):
        md = hashlib.md5()
        md.update(data.encode(encoding))
        data_md5 = md.hexdigest()
        return {'error': 0, 'data': data_md5}
    else:
        return {'error': 1, 'data': None, 'msg': "参数为非字符串数据,请重新确定!"}


# 2.获取随机密码
def get_password(len=8):
    psl = "0123456789abcdefghijklmnopqrstuvwxyz"
    password = random.sample(psl, len)
    return {"error": 0, "data": "".join(password)}


def test():
    # 检测字符编码格式
    msg = "demo"
    md = get_md5(msg)['data']
    pwd = get_password(16)['data']
    msg_d = md + msg
    pwd_new = add_to_16(pwd)
    msg_new = add_to_16(msg_d)
    aes = AES.new(pwd.encode("utf8"), AES.MODE_ECB)  # 初始化加密器
    data = aes.encrypt(msg_new.encode("utf8"))

    # 密钥对
    key = RSA.generate(2048)
    public_pem = key.publickey().exportKey()
    private_pem = key.exportKey()
    # 生成密钥并保存
    with open("mykey1.key", "wb") as f:
        f.write(private_pem)

    # 生成公钥并保存
    with open('mykey1.pub', 'wb') as f:
        f.write(public_pem)

    from Crypto.Cipher import PKCS1_v1_5 as p
    d = p.new(public_pem)
    # print(public_pem.decode("utf8"))
    # 私钥加密数字摘要
    c = pk.new(RSA.import_key(private_pem.decode("utf8")))
    md_l = c.encrypt(pwd_new.encode("utf8"))
    da_l = md_l + msg_new.encode("utf8")
    msg_l = aes.encrypt(da_l)
    msg_r = msg_new.encode("utf8") + msg_l
    print(msg_r)


# 密钥转成十六进制
def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return text


if __name__ == '__main__':
    msg = "demo"
    md = get_md5(msg)['data']
    pwd = get_password(16)['data']
    pwd = add_to_16(pwd)
    msg = add_to_16(msg)
    # 加载密钥
    with open("mykey.key", "r") as f:
        mykey = f.read()
    with open("mykey1.pub", "r") as f:
        otherkey = f.read()
    # 私钥加密数字摘要
    pr = pk.new(RSA.import_key(mykey))
    md_r = pr.encrypt(md.encode("utf8"))
    print(len(md_r), msg)
    # 对称加密数据和数字摘要
    aes = AES.new(pwd.encode("utf8"), AES.MODE_ECB)  # 初始化加密器
    data = aes.encrypt(md_r + msg.encode("utf8"))
    # 对方公钥加密随机密码
    pu = pk.new(RSA.import_key(otherkey))
    pwd_new = pu.encrypt(pwd.encode("utf8"))
    print(len(pwd_new + data), type(pwd_new + data))
    import base64

    test = base64.b64encode(pwd_new + data)
    print(type(test), len(test))
    print("*" * 50)
    # 解密过程
    # 1.解密base64
    t1 = base64.b64decode(test)
    # 使用公钥解密对称密码
    with open("mykey1.key", "r") as f:
        potherkey = f.read()
    pu1 = pk.new(RSA.import_key(potherkey))
    p, d = t1[0:256], t1[256:]
    p1 = pu1.decrypt(p)
    # 使用随机密码解密数据
    aes = AES.new(p1, AES.MODE_ECB)  # 初始化加密器
    d = aes.decrypt(d)
    m, dd = d[0:256], d[256:]
    # 使用公钥解密数据
    print(dd.decode("utf-8"))
