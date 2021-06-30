import csv
import json
import yaml
import configparser
import os
import re

"""
文件读写方法封装

"""


# 读取文件方法封装
def get_root_path():
    # 通过此模块文件路径获取项目根目录绝对路径
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/"
    return root_path


# 读文件
def read_file(file_path):
    """
    读取文件方法

    :param file_path: 从项目根路径节点开始的路径地址(不含项目绝对路径)
    :return: 文件内容
    """
    try:
        file_ext = re.findall(r"\..+", file_path)[0]
        print(f"文件后缀为{file_ext}")
        if file_ext == ".json":
            file_content = read_json(file_path)
            print("待读取的是json文件")
            return file_content
        if file_ext == ".yaml":
            file_content = read_yaml(file_path)
            return file_content
        if file_ext == ".ini":
            file_content = read_ini(file_path)
            return file_content
    except Exception as e:
        raise e


# json文件解析
def read_json(file_path):
    """
    json文件读取方法封装

    :param file_path: 从项目根路径节点开始的路径地址(不含项目绝对路径)
    :return: 文件内容
    """
    file_path = get_root_path() + file_path  # 拼装文件绝对路径
    with open(file_path, encoding="UTF-8") as f:
        json_content = json.load(f)
    return json_content


# yaml文件解析
def read_yaml(file_path):
    """
    yaml文件读取方法封装

    :param file_path: 从项目根路径节点开始的路径地址(不含项目绝对路径)
    :return: 文件内容
    """
    file_path = get_root_path() + file_path  # 拼装文件绝对路径
    with open(file_path, encoding="UTF-8") as f:
        yaml_content = yaml.safe_load(f)
    return yaml_content


# config文件解析
def read_ini(file_path):
    """
    ini文件读取方法封装

    :param file_path: 从项目根路径节点开始的路径地址(不含项目绝对路径)
    :return: 文件内容
    """
    file_path = get_root_path() + file_path  # 拼装文件绝对路径
    config = configparser.ConfigParser()
    config.read(file_path, encoding="UTF-8")
    # 将读取到的配置文件内容转化成字典
    config_dict = {}  # 初始化配置文件字典
    for section in config.sections():
        option_dict = {}  # 初始化配置文件option字典
        for option in config.options(section):
            option_dict[option] = config[section][option]
            config_dict[section] = option_dict
            # print(config_dict)
    return config_dict  # 返回字典格式的ini配置文件内容


def write_csv(write_data, file_path):
        keys = []
        # mongo查询结果首行表头字段缺失问题，遍历查询结果列表，获取其中最长字段长度的一个结果的索引
        for x in db_get_result:
            l = len([x for x in list(x.keys())])
            keys.append(l)
        enumer_list = list(enumerate(keys))
        enumer_list.sort(reverse=True, key=lambda x: x[1])
        max_fileds = enumer_list[0][0]
        if not db_get_result == []:
            csv_data = []
            fields = tuple([x for x in db_get_result[max_fileds]])
            # print(fields)
            csv_data.append(fields)
            for i in write_data:
                results = i.values()
                x = [str(y) for y in list(results)]
                csv_data.append(tuple(x))
            f = open(file_path, "w", encoding="GBK", newline="")
            writer = csv.writer(f)
            for i in csv_data:
                writer.writerow(i)
            f.close()
        else:
            print("数据库查询结果为空")