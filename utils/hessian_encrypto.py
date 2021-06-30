# -*- coding:utf-8 -*-
"""
# File       : hessian_encrypto
# Time       : 2021/5/29 13:47
# Author     : zhangjianfeng
# Version    : python 3.9
# Description:
"""
from pyhessian.client import HessianProxy

url = "http://example.com/hession4.0server/remote/helloSpring"
proxy = HessianProxy(url)
proxy.setName("zhangsan")  # 设置属性
print(proxy.sayHello())  # 调用方法
