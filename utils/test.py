# -*- coding:utf-8 -*-
"""
# File       : docleverApiToCsv.py
# Time       : 2021/6/1 16:43
# Author     : zhangjianfeng
# Version    : python 3.9
# Description:
"""
import json
import re


def bubble_sort(l_input):
    for i in range(len(l_input))[::-1]:
        for j in range(i):
            if l_input[j] > l_input[j + 1]:
                l_input[j], l_input[j + 1] = l_input[j + 1], l_input[j]
    l_sorted = l_input
    return l_sorted


def duplicate_rm(l_input):
    l_duplicate_rm = list(set(l_input))
    # l_duplicate_rm.sort()
    l_duplicate_rm.sort(key=lambda x: l_input.index(x))
    return l_duplicate_rm


def list_item_count_rank(l_input: list):
    l_items = set(l_input)
    item_dict = {}
    for i in l_items:
        item_dict[i] = l_input.count(i)
    cout_rank = sorted(item_dict.items(), key=lambda x: x[1], reverse=True)
    rank_dict = {}
    for i in cout_rank:
        rank_dict[i[0]] = i[1]
    print(rank_dict)
    return cout_rank


def quick_sort_th(array, left, right):
    if left >= right:
        return
    low = left
    high = right
    key = array[low]
    while left < right:
        while left < right and array[right] > key:
            right -= 1
        array[left] = array[right]
    while left < right and array[left] <= key:
        left += 1
    array[right] = array[left]
    array[right] = key
    quick_sort(array, low, left - 1)
    quick_sort(array, left + 1, high)


lll = [1, 9, 4, 33, 9, 7, 1, 6, 15, 18]
# # print(bubble_sort(l))
# # print(duplicate_rm(l))
# # print(list_item_count_rank(l))
# # print(quick_sort(lll))
# quick_sort_th(lll)
# print(lll)
# x = lambda *args:'必选' if x == 1
# print(x(1))
# import keyword
#
# print(keyword.kwlist)

# quick_sort = lambda array: array if len(array) <= 1 else \
#     quick_sort([item for item in array[1:] if item <= array[0]]) + [array[0]] + quick_sort([item for item in array[1:] if item > array[0]])

#
# must = lambda must: "必选" if must == 1 else "非必选"
#
# print(must(0))
t = {'mysql': {'ysapp': {'host': '10.213.40.118', 'port': 3306, 'user': 'ysapp_boss', 'pwd': '12Fj2uix)iu'}}}
# sql = "INSERT INTO TEST_TB1(ID, NAME) VALUES(1, 'name_insert1')"
# sql = "SELECT INTO TEST_TB1(ID, NAME) VALUES(1, 'name_insert1')"
# sql = "UPDATE INTO TEST_TB1(ID, NAME) VALUES(1, 'name_insert1')"
sql = "DELETE INTO TEST_TB1(ID, NAME) VALUES(1, 'name_insert1')"


# print(str(t).replace('\'', '"').strip())
# try:
#     if not re.search(r"^UPDATE", sql, re.IGNORECASE) is None:
#         print("语法正确", re)
#     else:
#         print(f"sql语法有误，请检查sql语法\n【{sql}】")
# except Exception as e:
#     raise e


# sql语法检查
def sql_async_check(func):
    def wraper(*args, **kwargs):
        try:
            sql = args[0]
            if not re.search(r"^UPDATE", sql, re.IGNORECASE) is None:
                return func(*args, **kwargs)
            else:
                print(f"sql语法有误，请检查sql语法\n【{sql}】")
        except Exception as e:
            raise e

    # return wraper


@sql_async_check
def test(sql):
    print("haha")


with open("D:\\00_pyprojects\\MyUtils\\utils\\module.json", encoding="UTF-8") as f:
    json_content = json.load(f)
print(json_content)
