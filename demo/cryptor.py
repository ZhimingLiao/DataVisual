# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州富力海珠城3810  志明  2019-09-11 15:08
# 当前计算机登录名称 :andy
# 项目名称  :DataVisual
# 编译器   :PyCharm
# ==================================================
# 生成RSA公钥和密钥,并且根据需要默认保存至临时文件
# rsa使用用法参考api:https://stuvel.eu/python-rsa-doc/usage.html
# ==================================================

__author____ = 'Andy Liao'
__time__ = '2019-09-11 15:08'
__all__ = ('Cryptor',)
__version__ = "1.0"

import os
import random

import rsa
# 以下模块需要下载Crypto,非系统自带模块
from Crypto.Cipher import AES


class Cryptor:

    def __init__(self, len_key, pwd):
        self.__len = int(len_key / 8)
        self.__pwd = pwd
        self.__RSA = rsa.newkeys(len_key, poolsize=1)

    def e(self, data, key, method="MD5"):
        # 1.得到文件数据签名,数据为字节码
        data = self.__add_to_16(data)
        sign = rsa.sign(data, self.__RSA[1], method)
        # 2.使用发送者私钥加密数字签名
        # 3.对称随机密码加密数字签名和数据内容
        aes = AES.new(self.__add_to_16(self.__pwd), AES.MODE_ECB)  # 初始化加密器
        data = aes.encrypt(sign + data)
        # 4.使用接收者公钥加密随机对称密码
        pwd_safe = rsa.encrypt(self.__add_to_16(self.__pwd), key)
        return pwd_safe + data

    def d(self, data, key):
        # 1.解密得到对称随机密码和数据以及数字摘要
        pwd, data = data[0: self.__len], data[self.__len:]
        pwd = rsa.decrypt(pwd, self.__RSA[1])
        # 2.得到数字签名和数据内容
        aes = AES.new(pwd, AES.MODE_ECB)  # 初始化加密器
        data = aes.decrypt(data)
        sign, datas = data[0:self.__len], data[self.__len:]
        # 3.验证数据内容以及解密返回数据是否修改
        try:
            rsa.verify(datas, sign, key)
        except rsa.pkcs1.VerificationError:
            return {"error": 1, msg: "警告:数据被修改,签名验证失败!"}
        else:
            return datas.decode("utf8")

    # 密钥转成十六进制,返回字节码

    def __add_to_16(slef, data):
        """
        :return:
        """
        while len(data) % 16 != 0:
            data += '\0'
        return data.encode("utf8")

    # 2.获取随机密码
    @staticmethod
    def get_password(len=8):
        psl = "0123456789abcdefghijklmnopqrstuvwxyz"
        password = random.sample(psl, len)
        return "".join(password)

    @property
    def pubkey(self):
        return self.__RSA[0]

    def save(self, pubkey=1, filename="public.key"):
        if not os.path.exists(filename):
            pass
        if pubkey == 1:
            with open(filename, "wb") as f:
                f.write(rsa.PublicKey.save_pkcs1(self.__RSA[0], format="PEM"))
        if pubkey == 2:
            with open(filename, "wb") as f:
                f.write(rsa.PrivateKey.save_pkcs1(self.__RSA[1], format="PEM"))
        return True

    # 从文件中加载公钥或私钥
    def load(self, pubkey=1, filename="public.key"):
        if not os.path.exists(filename):
            return {"error": 2, "msg": "不存在此文件!请更新!"}
        content = None
        with open(filename, "rb") as f:
            content = f.read()
        try:
            if pubkey == 1:
                key = rsa.PublicKey.load_pkcs1_openssl_pem(content)
            if pubkey == 2:
                key = rsa.PrivateKey.load_pkcs1(content)
        except ValueError:
            return {"error": 3, "msg": "参数不对,文件内容可能为公钥,但是参数为私钥!"}
        return key


if __name__ == '__main__':
    # rsa使用用法参考api:https://stuvel.eu/python-rsa-doc/usage.html
    t = Cryptor(1024, Cryptor.get_password())
    t1 = Cryptor(1024, Cryptor.get_password())
    msg = "demo"
    tt = t.e(msg, t1.pubkey)
    # t.save(pubkey=)
    print(t.load(pubkey=2))
