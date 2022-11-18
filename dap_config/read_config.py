# -*- coding: utf-8 -*-
import configparser
import logging
import os
import time
import yaml


class Read_Config:
    def __init__(self, configpath):
        self.back_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + configpath
        self.config = configparser.ConfigParser()
        self.config.read(self.back_path)

    def read_dbini(self, dba):
        db_dicts = {'host': self.config[dba]['host'],
                    'port': int(self.config[dba]['port']),
                    'user': self.config[dba]['user'],
                    'password': self.config[dba]['password'],
                    'database': self.config[dba]['database'],
                    'charset': self.config[dba]['charset']}
        return db_dicts
        # host = self.config[db]['host']
        # port = int(self.config[db]['port'])
        # user = self.config[db]['user']
        # password = self.config[db]['password']
        # database = self.config[db]['database']
        # charset = self.config[db]['charset']
        # con = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
        #                       charset=charset)
        # cur = con.cursor()
        # return cur

    def read_emailini(self, email):
        mail_dicts = {'SMTP_SSL': self.config[email]['SMTP_SSL'],
                      'port': self.config[email]['port'],
                      'user': self.config[email]['user'],
                      'password': self.config[email]['password'],
                      'sender': self.config[email]['sender'],
                      'receive': self.config[email]['receive'],
                      'Cc': self.config[email]['Cc']}
        return mail_dicts
        # con = smtplib.SMTP_SSL(SMTP_SSL, int(port))
        # login = con.login(user=user, password=password)
        # return login

    def api_log(self):
        # sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print(sys_path)
        # log_path = sys_path + '\log' + time.strftime('%Y-%m-%d', time.localtime()) + '.log'
        # backPath =  "/log/"
        if not os.path.exists(self.back_path):
            os.mkdir(self.back_path)
        log_time = time.strftime("%Y_%m_%d")

        log_name = self.back_path + log_time + '.log'
        print(log_name)
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        # 设置FileHandler日志文件
        fh = logging.FileHandler(log_name, 'w',
                                 encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # 设置控制台输出log
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        log.addHandler(fh)
        log.addHandler(ch)
        # 添加下面一句，在记录日志之后移除句柄
        # log.removeHandler(ch)
        # log.removeHandler(fh)
        # 关闭文件
        fh.close()
        ch.close()
        return log


if __name__ == '__main__':
    db = Read_Config('/dap_config/db.ini').read_dbini('dap_db')
    con = Read_Config('/dap_config/email.ini').read_emailini('email')

    print(db['host'])
    print(con['SMTP_SSL'])
