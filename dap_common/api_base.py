import requests
from dap_common.api_logger import api_log
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from dap_config.read_config import Read_Config


class HttpClient:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings()

    def __init__(self):
        self.__session = requests.session()
        # self.log = api_log()
        self.log = Read_Config('/log/').api_log()

    def get(self, url, **kwargs):
        return self.__request(url, 'GET', **kwargs, verify=False)

    def post(self, url, **kwargs):
        return self.__request(url, 'POST', **kwargs, verify=False)

    def __request(self, url, method, data=None, json=None, **kwargs):
        try:
            resp = None
            if method == 'POST':
                resp = self.__session.post(url, data, json, **kwargs)
                if resp.status_code == 200:
                    self.log.info('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
                else:
                    self.log.error('DAP_URL:{0},响应状态码:{1},返回值:{2}'.format(resp.url, resp.status_code, resp.json()))
            elif method == 'GET':
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


if __name__ == '__main__':
    http = HttpClient()
    url = "https://172.16.2.51:58443/back/dap/index/domain/page"
    header = {
        # "X-CSRF-TOKEN": "fbda12c2-2288-4bd2-b141-e2f3674ade52-70073417",
        "Cookie": "JSESSIONID=4579d2b4-a0bc-49ff-ad14-948e364aae56-63528364",
        "Content-Type": "application/json;"
    }
    page = http.post(url, headers=header, json={})

    url2 = "https://172.16.2.51:58443/back/dap/index/domain/page1"
    page_domain = http.post(url2, headers=header, json={})

    url3 = "https://172.16.2.51:58443/back/dap/index/dataanalysis/columns?id=2&tableName=area_copy1"

    page_dataanalysis = http.get(url3, headers=header)
