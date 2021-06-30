# -*- coding:utf-8 -*-
"""
File       : docleverApiToCsv.py
Time       : 2021/6/21 15:25
Author     : zhangjianfeng
Version    : python 3.9
Description: Doclever接口文档导出json转csv表格，使用方法(命令行)：python docleverApiToCsv.py json文档路径
"""
import csv
import json
import os
import sys
import time


class DocleverToCsv:

    def __init__(self, file_path):
        """
        doclever导出json文档内容读取

        :param file_path: 接口json文档路径
        :return: json文档原始数据，“data”内容
        """
        with open(file_path, encoding="UTF-8") as f:
            json_content = json.load(f)
        self.docName = str(file_path).split('\\')[-1].split('.')[0]
        self.api_groups = json_content['data']

    def data_content(self, api_groups, groups: list = None):
        """
        doclever导出json文档“data”内容，格式化提取

        :param groups: 请求参数列表提取容器，用于写入csv
        :return: 请求参数列表格式化提取后的列表，字段内容有【('name', 'urlPath', 'header', 'body', 'createdAt', 'updatedAt')】
        """
        if groups is None:
            groups = []
        for i in api_groups:
            if 'data' not in [x for x in i.keys()]:
                request_header = {}
                for x in i['param'][0]['header']:
                    request_header[x['name']] = x['value']
                request_header_format = json.dumps(request_header, indent=4, ensure_ascii=False, sort_keys=False,
                                                   separators=(',', ':'))
                request_body = {}
                request_doc = ()
                try:
                    if i['param'][0]['bodyInfo']:
                        bodyInfo = i['param'][0]['bodyInfo']
                        if 'rawJSON' in [t for t in bodyInfo.keys()]:
                            for y in bodyInfo['rawJSON']:
                                request_body[y['name']] = y['remark']
                        else:
                            bodyParam = i['param'][0]['bodyParam']
                            for y in bodyParam:
                                request_body[y['name']] = y['remark']
                        request_body_format = json.dumps(request_body, indent=4, ensure_ascii=False, sort_keys=False,
                                                         separators=(',', ':'))
                        request_doc = (
                        i['name'], i['url'], request_header_format, request_body_format, i['createdAt'], i['updatedAt'])
                except:
                    request_doc = (i['name'], i['url'], request_header_format, '{}', i['createdAt'], i['updatedAt'])
                groups.append(request_doc)
            else:
                self.data_content(i['data'], groups)
        return groups

    def apidoc_to_csv(self, row_data: list):
        """
        列表写入csv

        :param row_data: 原始列表数据，列表内元素对应列内容，格式[(),(),()]
        :return: 写入csv到当前文件同路径下，
        """
        fields = ('name', 'urlPath', 'header', 'body', 'createdAt', 'updatedAt')
        if not row_data == []:
            csv_data = []
            csv_data.append(fields)
            for i in row_data:
                csv_data.append(i)
            csv_path = f"{os.path.abspath('.')}\\{self.docName}_{time.strftime('%Y%m%d%H%M%S')}.csv"
            file = open(csv_path, "w", encoding="GBK", newline="")
            writer = csv.writer(file)
            for i in csv_data:
                writer.writerow(i)
            print(f"json文档接口描述内容已转为csv，路径：{csv_path}")
            file.close()
        else:
            print("数据列表为空，请检查输入文件内容")


if __name__ == "__main__":
    file_path = sys.argv[1]
    csv_write = DocleverToCsv(file_path)
    d_print = csv_write.data_content(csv_write.api_groups)
    csv_write.apidoc_to_csv(d_print)
