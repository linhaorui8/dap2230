import datetime
import json
import os
import pickle

import yaml

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(path)


def load_yaml(file_path):
    try:
        data_file_path = os.path.join(path, 'dap_data', file_path)
        with open(data_file_path, mode='r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        print('打开yaml文件异常', e)
    else:
        return data
    finally:
        f.close()

def write_yaml(values):
    try:
        file_path = 'token.yaml'
        data_file_path = os.path.join(path, 'dap_data', file_path)
        with open(data_file_path, mode='w+', encoding='utf-8') as tf:
            json.dump(values, tf, indent=4,ensure_ascii=False)
    except Exception as e:
        print('写入yaml文件异常', e)
    finally:
        tf.close()

#
# dics = {"get_header": {'X-CSRF-TOKEN': 'f52ae5f4-a236-4360-89bf-0c84231d5e97-36602184',
#                        'Cookie': 'JSESSIONID=d3e44d0e-33b1-4792-a766-9e5fc42f5048-85507811'}}
# dic1 ={"post_header": {
#           "X-CSRF-TOKEN": "66dc63ed-1954-4085-8f3a-cc2d56f23081-35612687",
#           "Cookie": "JSESSIONID=e44b7deb-0845-4356-a638-c46e79ba7774-60332709",
#           'Content-Type': 'application/json;'}}
# # print(type(dics))
# write_yaml(dics)
# write_yaml(dic1)

# data = write_yaml('login.yaml',file_write)
#
# data=load_yaml('sms_home.yaml')
# print(data['home_url'])
# data = load_yaml('login.yaml')
# print(data['login_data'])
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#report_file = r'2022-11-04 18-report.html'
current_date = datetime.datetime.now().strftime("%Y-%m-%d %H")
report_dir = r'report'  # 保存路径
report_file = current_date + r'-report.html'
report_file_path = os.path.join(path, r'testcase\report', report_file)
print(report_file_path)
email_file = r'email.ini'
email_file_path = os.path.join(path, r'api_base', email_file)
print(email_file_path)
datas=load_yaml('test.yaml')
print(datas['a'])