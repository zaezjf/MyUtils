import os
import pymongo
import cx_Oracle as cx
import pymysql


class DbBass:
    # 数据库登录配置信息

    def __init__(self, db_type, db_client, db_name, db_userName, db_userPwd):
        """
        数据库配置信息

        :param db_type: 数据库类型（mysql，oracle，mongo）
        :param db_client: 数据库地址，IP:端口(xxx.xxx.xxx.xx:xxxx)
        :param db_name: 数据库名
        :param db_userName: 数据库连接，登录用户
        :param db_userPwd: 数据库连接，登录用户密码
        """
        self.db_type = db_type
        self.db_name = db_name
        self._db_client = {db_type: {db_name: {}}}
        self._db_client[db_type][db_name]['host'] = (db_client.split(':'))[0]
        self._db_client[db_type][db_name]['port'] = int((db_client.split(':'))[1])
        self._db_client[db_type][db_name]['user'] = db_userName
        self._db_client[db_type][db_name]['pwd'] = db_userPwd
        print(self._db_client)

    # 数据库连接
    def db_connect(self):
        db_type = self.db_type
        db_name = self.db_name
        if db_type == "mongo":
            db_conf = self._db_client[db_type][db_name]
            db_host = db_conf["host"]
            db_port = db_conf["port"]
            db_user = db_conf["user"]
            db_pwd = db_conf["pwd"]
            db_uri = f"mongodb://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
            print(db_uri)
            db = pymongo.MongoClient(db_uri)
            # client = pymongo.MongoClient(db_host, db_port)
            # db.authenticate(db_user, db_pwd, mechanism='SCRAM-SHA-1')
            print(f">>>连接数据库<<<\n数据库类型:[{db_type}]\n数据库:[{db_name}]\n{db_host}:{db_port}\n登录用户:[{db_user}]")
            return db
        if db_type == "oracle":
            os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 设置系统环境变量
            db_conf = self._db_client[db_type][db_name]
            db_host = db_conf["host"]
            db_port = db_conf["port"]
            db_user = db_conf["user"]
            db_pwd = db_conf["pwd"]
            db_ser = db_conf["service"]
            db_uri = f"{db_host}:{db_port}/{db_ser}"
            db = cx.connect(db_user, db_pwd, db_uri)  # oracle数据库连接方法import cx_Oracle as cx
            if __name__ == "__main__":
                print(f">>>连接数据库<<<\n数据库类型:[{db_type}]\n数据库:[{db_name}]\n{db_uri}\n登录用户:[{db_user}]")
            # print(db)
            return db
        if db_type == "mysql":
            db_conf = self._db_client[db_type][db_name]
            db_host = db_conf["host"]
            db_port = db_conf["port"]
            db_user = db_conf["user"]
            db_pwd = db_conf["pwd"]
            db_uri = f"{db_host}:{db_port}"
            db = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_pwd,
                                 database=db_name)  # mysql数据库连接方法
            if __name__ == "__main__":
                print(f">>>连接数据库<<<\n数据库类型:[{db_type}]\n数据库:[{db_name}]\n{db_uri}\n登录用户:[{db_user}]")
            # print(db)
            return db

    # 获取数据库数据，sql查询
    def get_dbData(self, sql, mongo_collection: list = None):
        """
        sql查询

        :param db_type: 连接数据库类型
        :param db_name: 连接的数据库名
        :param sql: sql语句
        :param mongo_collection: mongoDb需要传入数据库库名和表名的列表：[库名, 表名]
        :return: 格式化查询结果，列表格式字典集合，按行展示列名对应字段，例：[{列名1:值, 列名2:值,},{列名1:值, 列名2:值}]
        """
        db_type = self.db_type
        db_name = self.db_name
        if db_type == "mongo":
            db = self.db_connect()
            collection = db[mongo_collection[0]][mongo_collection[1]]
            # print(ex.find_one())
            mongo_result = {}
            exec(f"mongo_result['x'] = [x for x in collection.{sql}]")
            res = mongo_result['x']
            db.close()
            if __name__ == "__main__":
                print("---数据库连接已关闭---")
            return res
        if db_type == "oracle":
            db = self.db_connect()
            cursor = db.cursor()
            ex = cursor.execute(sql)
            fields = ex.description
            result = ex.fetchall()
            # print(f"表列名：{fields}")
            # print(f"查询结果：{result}")
            # print(db[db_dbName][db_table])
            res = self.format_data(fields, result)
            cursor.close()
            db.close()
            if __name__ == "__main__":
                print("---数据库连接已关闭---")
            return res
        if db_type == "mysql":
            db = self.db_connect()
            cursor = db.cursor()
            ex = cursor.execute(sql)
            fields = cursor.description
            result = cursor.fetchall()
            # print(fields)
            # print(result)
            # print(f"表列名：{fields}")
            # print(f"查询结果：{result}")
            # print(db[db_dbName][db_table])
            res = self.format_data(fields, result)
            cursor.close()
            db.close()
            if __name__ == "__main__":
                print("---数据库连接已关闭---")
            return res

    # 获取数据库数据，sql查询
    def del_mysql(self, sql):
        """
        sql查询

        :param db_type: 连接数据库类型
        :param db_name: 连接的数据库名
        :param sql: sql语句
        :param mongo_collection: mongoDb需要传入数据库库名和表名的列表：[库名, 表名]
        :return: 格式化查询结果，列表格式字典集合，按行展示列名对应字段，例：[{列名1:值, 列名2:值,},{列名1:值, 列名2:值}]
        """
        db_type = self.db_type
        db_name = self.db_name
        if db_type == "mysql":
            db = self.db_connect()
            cursor = db.cursor()
            try:
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
            except Exception as e:
                raise e

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
    db_client = "10.213.40.118:3306"
    db_type = "mysql"
    db_name = 'ysapp'
    db_userName = "ysapp_boss"
    db_userPwd = "12Fj2uix)iu"
    sql_func = "select"
    sql = "SELECT * FROM sf_app_register WHERE MOBILE  LIKE '184%'"
    db = DbBass(db_type, db_client, db_name, db_userName, db_userPwd)
    debug_print = db.get_dbData(sql)
    print(debug_print)
