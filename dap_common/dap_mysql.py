import pymysql

from dap_config.read_config import Read_Config


class MysqlDB:
    def __init__(self):
        # self.read_config = Read_Config(configpath)
        # 初始化 连接dap数据库
        self.cur = Read_Config('/dap_config/db.ini').read_dbini('dap_db')
        self.con = pymysql.connect(host=self.cur['host'], port=self.cur['port'], user=self.cur['user'],
                                   password=self.cur['password'], database=self.cur['database'],
                                   charset=self.cur['charset'])
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()
        # 1.连接  2.创建游标 3.写sql语句  4.执行sql  5.获得结果
        # 查询语句

    def get_all(self, sql):
        global ret
        try:
            self.cur.execute(sql)
            ret = self.cur.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return ret

    def get_one(self, sql):
        global ret
        try:
            self.cur.execute(sql)
            ret = self.cur.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return ret

    def edit(self, sql):
        try:
            self.cur.execute(sql)
            self.cur.execute('commit')
            self.close()
        except Exception as e:
            print(e)
        return True


if __name__ == '__main__':
    db = MysqlDB()

    print(db.get_one('select * from dap_data_source'))
