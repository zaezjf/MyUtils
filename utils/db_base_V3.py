# -*- coding:utf-8 -*-
"""
File       : db_base_V3
Time       : 2021/6/29 17:49
Author     : zhangjianfeng
Version    : python 3.9
Description: 
"""
import os
import re
import sys
import pymongo
import cx_Oracle as cx
import pymysql


class DbBass:

    def __init__(self, db_config: str):
        """
        数据库连接配置信息读取

        :param db_config: 数据库连接配置信息格式："db_type=xxxx&db_client=xxx.xxx.xxx.xxx:xxxx&db_name=xxxx&db_userName=xxxx
        &db_userPwd=xxxx&db_service=orcl"
        """
        # 获取数据库连接配置信息，并格式化保存为列表[(key,value)……]
        db_config_items = [((items.split("="))[0], (items.split("="))[1]) for items in
                           [x for x in db_config.split("&")]]
        # 读取配置信息键值对
        temp_dict = {key: value for (key, value) in db_config_items}
        self._db_client = {temp_dict["db_type"]: {temp_dict["db_name"]: {}}}
        # 数据库配置信息转存为字典，格式：{"mysql":{"ysapp":{"host":"10.213.40.118","port":3306,"user":"ysapp_boss","pwd":"12Fj2uix)iu"}}}
        self.db_type = temp_dict["db_type"]
        self.db_name = temp_dict["db_name"]
        self._db_client[self.db_type][self.db_name]['host'] = ((temp_dict['db_client']).split(':'))[0]
        self._db_client[self.db_type][self.db_name]['port'] = int((temp_dict['db_client'].split(':'))[1])
        self._db_client[self.db_type][self.db_name]['user'] = temp_dict['db_userName']
        self._db_client[self.db_type][self.db_name]['pwd'] = temp_dict['db_userPwd']
        if self.db_type == "oracle":
            self._db_client[self.db_type][self.db_name]['service'] = temp_dict['db_service']
        # print(self._db_client)

    # 数据库连接
    def db_connect(self):
        db_type = self.db_type
        db_name = self.db_name
        db_conf = self._db_client[db_type][db_name]
        db_host = db_conf["host"]
        db_port = db_conf["port"]
        db_user = db_conf["user"]
        db_pwd = db_conf["pwd"]
        if db_type == "mongo":
            db_uri = f"mongodb://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
            # print(db_uri)
            try:
                db = pymongo.MongoClient(db_uri)
                # client = pymongo.MongoClient(db_host, db_port)
                # db.authenticate(db_user, db_pwd, mechanism='SCRAM-SHA-1')
                # print(f">>>连接数据库<<<\n数据库类型:[{db_type}]\n数据库:[{db_name}]\n{db_host}:{db_port}\n登录用户:[{db_user}]")
                return db
            except Exception as e:
                print(f"数据库连接异常，连接配置信息{self._db_client}")
                raise e
        if db_type == "oracle":
            os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 设置系统环境变量
            db_ser = db_conf["service"]
            db_uri = f"{db_host}:{db_port}/{db_ser}"
            try:
                db = cx.connect(db_user, db_pwd, db_uri)  # oracle数据库连接方法import cx_Oracle as cx
                return db
            except Exception as e:
                print(f"数据库连接异常，连接配置信息{self._db_client}")
                raise e
        if db_type == "mysql":
            db_uri = f"{db_host}:{db_port}"
            try:
                db = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_pwd,
                                     database=db_name)  # mysql数据库连接方法
                return db
            except Exception as e:
                print(f"数据库连接异常，连接配置信息{self._db_client}")
                raise e

    # 数据库表内容查询
    def select_db(self, sql, mongo_collection: str = None):
        """
        sql查询

        :param sql: sql语句
        :param mongo_collection: mongoDb需要传入需要查询的集合表名
        :return: 格式化查询结果，列表格式字典集合，按行展示列名对应字段，例：[{列名1:值, 列名2:值,},{列名1:值, 列名2:值}]
        """
        db_type = self.db_type
        db_name = self.db_name
        if db_type == "mongo":
            if not re.search(r"^FIND", sql, re.IGNORECASE) is None:
                pass
            else:
                raise AttributeError(f"sql语法有误，请检查sql语法\n【{sql}】")
            # mongoDb表查语法参考官方文档，此处对语法进行格式规范，格式示例: 查询所有数据：find({}) ，查询
            db = self.db_connect()
            if not mongo_collection is None:
                collection = db[db_name][mongo_collection]
                mongo_result = {}
                exec(f"mongo_result['x'] = [x for x in collection.{sql}]")
                res = mongo_result
                db.close()
                return res
            else:
                print("mongoDb需要指定查询表(集合)")
                raise AttributeError("缺少mongo_collection参数")
        if db_type == "oracle" or db_type == "mysql":
            if not re.search(r"^SELECT", sql, re.IGNORECASE) is None:
                pass
            else:
                raise AttributeError(f"sql语法有误，请检查sql语法\n【{sql}】")
            db = self.db_connect()
            cursor = db.cursor()
            fields, result = '', ''
            ex = cursor.execute(sql)
            if db_type == "oracle":
                fields = ex.description
                result = ex.fetchall()
            elif db_type == "mysql":
                fields = cursor.description
                result = cursor.fetchall()
            res = self.format_data(fields, result)
            cursor.close()
            db.close()
            return res

    # 数据库表内容插入
    def insert_db(self, sql, mongo_collection: str = None):
        """
        sql查询

        :param sql: sql语句
        :return: Non
        """
        db_type = self.db_type
        db_name = self.db_name
        if not re.search(r"^INSERT", sql, re.IGNORECASE) is None:
            pass
        else:
            raise AttributeError(f"sql语法有误，请检查sql语法\n【{sql}】")
        if db_type == "mongo":
            db = self.db_connect()
            try:
                if not mongo_collection is None:
                    res = None
                    collection = db[db_name][mongo_collection]
                    if not re.search(r"^INSERT_ONE", sql, re.IGNORECASE) is None:
                        ex = eval(f"collection.{sql}")
                        res = ex.inserted_id
                    elif not re.search(r"^INSERT_MANY", sql, re.IGNORECASE) is None:
                        ex = eval(f"collection.{sql}")
                        res = ex.inserted_ids
                    print(f"数据插入成功: {res}")
                else:
                    print("mongoDb需要指定查询表(集合)")
                    raise AttributeError("缺少mongo_collection参数")
                db.close()
            except Exception as e:
                print(f"执行sql异常【{sql}】\n连接配置信息{self._db_client}")
                raise e
        if db_type == "oracle" or db_type == "mysql":
            db = self.db_connect()
            cursor = db.cursor()
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"执行sql异常【{sql}】\n连接配置信息{self._db_client}")
                raise e
            finally:
                cursor.close()
                db.close()

    # 数据库表内容更新
    def update_db(self, sql, mongo_collection: str = None):
        """
        sql查询

        :param sql: sql语句
        :return: Non
        """
        db_type = self.db_type
        db_name = self.db_name
        if not re.search(r"^UPDATE", sql, re.IGNORECASE) is None:
            pass
        else:
            raise AttributeError(f"sql语法有误，请检查sql语法\n【{sql}】")
        if db_type == "mongo":
            db = self.db_connect()
            try:
                if not mongo_collection is None:
                    res = None
                    collection = db[db_name][mongo_collection]
                    if not re.search(r"^UPDATE_ONE", sql, re.IGNORECASE) is None:
                        ex = eval(f"collection.{sql}")
                        res = ex.modified_count
                    elif not re.search(r"^UPDATE_MANY", sql, re.IGNORECASE) is None:
                        ex = eval(f"collection.{sql}")
                        res = ex.modified_count
                    print(f"[{res}]个文档已更新")
                else:
                    print("mongoDb需要指定查询表(集合)")
                    raise AttributeError("缺少mongo_collection参数")
                db.close()
            except Exception as e:
                print(f"执行sql异常【{sql}】\n连接配置信息{self._db_client}")
                raise e
        if db_type == "oracle" or db_type == "mysql":
            db = self.db_connect()
            cursor = db.cursor()
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"执行sql异常【{sql}】\n连接配置信息{self._db_client}")
                raise e
            finally:
                cursor.close()
                db.close()

    # 数据库表内容删除
    def delete_db(self, sql, mongo_collection: str = None):
        """
        sql查询

        :param sql: sql语句
        :return: Non
        """
        db_type = self.db_type
        db_name = self.db_name
        if not re.search(r"^DELETE", sql, re.IGNORECASE) is None:
            pass
        else:
            raise AttributeError(f"sql语法有误，请检查sql语法\n【{sql}】")
        if db_type == "mongo":
            db = self.db_connect()
            try:
                if not mongo_collection is None:
                    res = None
                    collection = db[db_name][mongo_collection]
                    if not re.search(r"^DELETE_ONE", sql, re.IGNORECASE) is None:
                        ex = eval(f"collection.{sql}")
                        res = ex.deleted_count
                    elif not re.search(r"^DELETE_MANY", sql, re.IGNORECASE) is None:
                        ex = eval(f"collection.{sql}")
                        res = ex.deleted_count
                    print(f"[{res}]个文档已删除")
                else:
                    print("mongoDb需要指定查询表(集合)")
                    raise AttributeError("缺少mongo_collection参数")
                db.close()
            except Exception as e:
                print(f"执行sql异常【{sql}】\n连接配置信息{self._db_client}")
                raise e
        if db_type == "oracle" or db_type == "mysql":
            db = self.db_connect()
            cursor = db.cursor()
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"执行sql异常【{sql}】\n连接配置信息{self._db_client}")
                raise e
            finally:
                cursor.close()
                db.close()

    # 数据格式化 fields 字段名，result 结果集
    def format_data(self, fields, result):
        # 字段数组，表列名
        field = []
        for i in fields:
            field.append(i[0])
        # 返回的数组集合形式[{'id': 1, 'name': 'admin', 'password': '123456'}]
        res = []
        for data in result:
            line_data = {}
            for index in range(0, len(field)):
                line_data[field[index]] = data[index]
            res.append(line_data)
        return res

    # 关闭数据库连接
    def db_close(self):
        db_type = self.db_type
        db = self.db_connect()
        if db_type == "mongo":
            db.close()
        else:
            db.cursor().close()  # 关闭数据库游标
            db.close()  # 关闭数据库连接


if __name__ == "__main__":
    # mongo_collection = None

    """mysql数据库调试数据"""
    # db_config_mysql = "db_type=mysql&db_client=10.213.40.118:3306&db_name=ysapp&db_userName=ysapp_boss&db_userPwd=12Fj2uix)iu"
    # db_func, db_sql_mysql = "insert", "INSERT INTO wbx_test(STUD_NAME,STUD_AGE,STUD_WEIGHT) VALUES('张三','18','90')"
    # db_func, db_sql_mysql = "update", "UPDATE wbx_test SET STUD_AGE = '30' WHERE STUD_NAME = '张三'"
    # db_func, db_sql_mysql = "select", "SELECT * FROM wbx_test WHERE STUD_NAME = '张三'"
    # db_func, db_sql_mysql = "delete", "DELETE FROM wbx_test WHERE STUD_NAME = '张三'"

    """oracle数据库调试数据"""
    # db_config_oracle = "db_type=oracle&db_client=10.213.32.74:1521&db_name=yspos_portal&db_userName=yspos_portal&db_userPwd=123456&db_service=orcl"
    # db_func, db_sql_oracle = "insert", "INSERT INTO WBXTEST(ID, NAME) VALUES(1,'NAME1')"
    # db_func, db_sql_oracle = "update", "UPDATE WBXTEST SET NAME = 'NAME2' WHERE NAME = 'NAME1'"
    # db_func, db_sql_oracle = "select",  "SELECT * FROM WBXTEST WHERE NAME = 'NAME2'"
    # db_func, db_sql_oracle = "delete", "DELETE FROM WBXTEST WHERE NAME = 'NAME2'"

    """mongoDb数据库调试数据"""
    mongo_collection = 'credb'
    # mongo_collection = 'mh_app_h5_use_stats'
    db_config_mongo = "db_type=mongo&db_client=10.213.40.58:27017&db_name=bottom&db_userName=bottomAdmin&db_userPwd=bottom1234567"
    # db_func, db_sql_mongo = "insert", 'insert_one({"name":"name_insert"})'
    # db_func, db_sql_mongo = "update", 'update_one({"name":"name_insert"},{"$set":{"name":"name_update"}})'
    db_func, db_sql_mongo = "select", 'find_one({"name":"name_update"})'
    # db_func, db_sql_mongo = "delete", 'delete_one({"name":"name_update"})'
    # db_func, db_sql_mongo = "insert", 'insert_many([{"name":"name_insert1"},{"name":"name_insert2"}])'
    # db_func, db_sql_mongo = "update", 'update_many({"name": {"$regex":".*insert.*"}},{"$set":{"name":"name_update"}})'
    # db_func, db_sql_mongo = "select", 'find({"name":"name_update"})'
    # db_func, db_sql_mongo = "delete", 'delete_many({"name": {"$regex": ".*insert.*"}})'

    """调试配置选择"""
    # db_config, db_sql = db_config_mysql, db_sql_mysql
    # db_config, db_sql = db_config_oracle, db_sql_oracle
    db_config, db_sql = db_config_mongo, db_sql_mongo

    db = DbBass(db_config)
    if db_func == "select":
        if not mongo_collection is None:
            debug_print = db.select_db(db_sql, mongo_collection)
        else:
            debug_print = db.select_db(db_sql)
        print(f"共查询到【{len(debug_print)}】条结果\n{debug_print}")
    elif db_func == "insert":
        if not mongo_collection is None:
            debug_print = db.insert_db(db_sql, mongo_collection)
        else:
            debug_print = db.insert_db(db_sql)
        print(debug_print)
    elif db_func == "update":
        if not mongo_collection is None:
            debug_print = db.update_db(db_sql, mongo_collection)
        else:
            debug_print = db.update_db(db_sql)
        print(debug_print)
    elif db_func == "delete":
        if not mongo_collection is None:
            debug_print = db.delete_db(db_sql, mongo_collection)
        else:
            debug_print = db.delete_db(db_sql)
        print(debug_print)
