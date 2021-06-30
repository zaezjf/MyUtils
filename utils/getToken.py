# -*- coding:utf-8 -*-
"""
File       : getToken.py
Time       : 2021/6/28 17:25
Author     : zhangjianfeng
Version    : python 3.9
Description: 
"""
import sys
import re


str1 = str(sys.argv[1])
# print(str1, type(str1))

pattern = r'token:(.+?),'
match = re.findall(pattern, str1)
# print(match)
print(match[0])

