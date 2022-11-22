import requests
from bs4 import BeautifulSoup
from dap_config.read_config import Read_Config
from dap_data.read_data import load_yaml, write_yaml


class HttpClient:

    def __init__(self):
        self.__session = requests.session()
        # self.log = api_log()
        self.log = Read_Config('/log/').api_log()
        self.login = load_yaml('login.yaml')

    def get(self, url, **kwargs):
        return self.__request(url, 'GET', **kwargs, verify=False)

    def post(self, url, **kwargs):
        return self.__request(url, 'POST', **kwargs, verify=False)

    def __request(self, url, method, data=None, json=None, **kwargs):
        try:
            resp = None
            if method == 'POST':
                requests.packages.urllib3.disable_warnings()
                resp = self.__session.post(url, data, json, **kwargs)
                if resp.status_code == 200:
                    self.log.info('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
                else:
                    self.log.error('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
            elif method == 'GET':
                requests.packages.urllib3.disable_warnings()
                resp = self.__session.get(url, **kwargs)
                if resp.status_code == 200:
                    self.log.info('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
                else:
                    self.log.error('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
            elif method == 'PUT':
                resp = self.__session.put(url, data, json, **kwargs)
                if resp.status_code == 200:
                    self.log.info('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
                else:
                    self.log.error('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
            elif method == 'DELETE':
                resp = self.__session.delete(url, **kwargs)
                if resp.status_code == 200:
                    self.log.info('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
                else:
                    self.log.error('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
            return resp
        except Exception as e:
            print('接口请求异常', e)

    def webkit_login(self):
        try:
            login_data = self.login['login_data']
            print(login_data)
            login_url = self.login['login_url']
            login_headers = self.login['headers']
            login_get = self.__session.get(login_url['url'])
            print(login_get)
            html_execution = BeautifulSoup(login_get.content, 'html.parser')
            execution = html_execution.findAll('input')[3].get('value')
            print(execution)
            login_data['execution'] = execution
            login_success = self.__session.post(login_url['url'], data=login_data, headers=login_headers
                                                , allow_redirects=False,verify=False)
            print(login_success.status_code)
            login_token = self.__session.get(login_success.headers['Location'], allow_redirects=False,verify=False)
            print(login_token.status_code)
            request_cookies = login_token.cookies.get_dict()
            print(request_cookies)
            # print(login_token.headers)
            get_cookies = 'JSESSIONID={0}'.format(request_cookies['JSESSIONID'])
            print(get_cookies)
            csrf_token = self.__session.get(login_url['get_token']).content
            # print(csrf_token)
            html_execution = BeautifulSoup(csrf_token, 'html.parser')
            csrf_token1 = html_execution.find('input').get('value')
            print(csrf_token1)
            header = {"get_header": {'X-CSRF-TOKEN': csrf_token1, 'Cookie': get_cookies},
                      "post_header": {'X-CSRF-TOKEN': csrf_token1, 'Cookie': get_cookies,
                                      'Content-Type': 'application/json;'}}

            write_yaml(header)
        except Exception as e:
            print('登录异常%s', e)


if __name__ == '__main__':
    http = HttpClient()
    http.webkit_login()
#     url = "https://172.16.2.51:58443/back/dap/index/domain/page"
#     header = {
#         # "X-CSRF-TOKEN": "fbda12c2-2288-4bd2-b141-e2f3674ade52-70073417",
#         "Cookie": "JSESSIONID=4579d2b4-a0bc-49ff-ad14-948e364aae56-63528364",
#         "Content-Type": "application/json;"
#     }
#     page = http.post(url, headers=header, json={})
#
#     url2 = "https://172.16.2.51:58443/back/dap/index/domain/page1"
#     page_domain = http.post(url2, headers=header, json={})
#
#     url3 = "https://172.16.2.51:58443/back/dap/index/dataanalysis/columns?id=2&tableName=area_copy1"
#
#     page_dataanalysis = http.get(url3, headers=header)
