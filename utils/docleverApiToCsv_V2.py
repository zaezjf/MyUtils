# -*- coding:utf-8 -*-
"""
File       : docleverApiToCsv_V2.py
Time       : 2021/6/22 16:37
Author     : zhangjianfeng
Version    : python 3.9
Description: Doclever接口文档导出json转csv表格，使用方法(命令行)：python docleverApiToCsv_V2.py json文档路径
ReleaseNote:
    V1: 1、解析接口文档接口请求方法，保存写入csv文件字段;
        2、解析接口请求参数是否必选，格式化并写入参数备注内容标记。
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
        with open('./tese.json', 'w') as f:
            f = f.write(json.dumps(self.api_groups, indent=4, ensure_ascii=False, sort_keys=False, separators=(',', ":")))

    def data_content(self, api_groups, groups: list = None):
        """
        doclever导出json文档“data”内容，格式化提取

        :param groups: 请求参数列表提取容器，用于写入csv
        :return: 请求参数列表格式化提取后的列表，字段内容有【('name', 'urlPath', 'method', 'header', 'body/param', 'createdAt', 'updatedAt')】
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
                    if i['method'] == 'POST':
                        bodyInfo = i['param'][0]['bodyInfo']
                        if 'rawJSON' in [t for t in bodyInfo.keys()]:
                            for y in bodyInfo['rawJSON']:
                                must = ''
                                if y['must'] == 1:
                                    must = '必选'
                                elif y['must'] == 0:
                                    must = '可选'
                                request_body[y['name']] = f"{y['remark']}({must})"
                        else:
                            quryParam = i['param'][0]['bodyParam']
                            for y in quryParam:
                                must = ''
                                if y['must'] == 1:
                                    must = '必选'
                                elif y['must'] == 0:
                                    must = '可选'
                                request_body[y['name']] = f"{y['remark']}({must})"
                        request_body_format = json.dumps(request_body, indent=4, ensure_ascii=False, sort_keys=False,
                                                         separators=(',', ':'))
                        request_doc = (i['name'], i['url'], i['method'], request_header_format, request_body_format,
                                       i['createdAt'], i['updatedAt'])
                    elif i['method'] == 'GET':
                        quryParam = i['param'][0]['queryParam']
                        for y in quryParam:
                            must = ''
                            if y['must'] == 1:
                                must = '必选'
                            elif y['must'] == 0:
                                must = '可选'
                            request_body[y['name']] = f"{y['remark']}({must})"
                        request_body_format = json.dumps(request_body, indent=4, ensure_ascii=False, sort_keys=False,
                                                         separators=(',', ':'))
                        request_doc = (i['name'], i['url'], i['method'], request_header_format, request_body_format,
                                       i['createdAt'], i['updatedAt'])
                except Exception as e:
                    print("接口文档json内容有误，请求方法非“POST/GET”，请检查")
                    raise e
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
        fields = ('name', 'urlPath', 'method', 'header', 'body/param', 'createdAt', 'updatedAt')
        if not row_data == []:
            csv_data = []
            csv_data.append(fields)
            for i in row_data:
                csv_data.append(i)
            csv_path = f"{os.path.abspath('.')}\\{self.docName}_{time.strftime('%Y%m%d%H%M%S')}.csv"
            print(csv_path)
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
    # d_print = csv_write.data_content(csv_write.api_groups)
    # csv_write.apidoc_to_csv(d_print)
