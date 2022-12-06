from itertools import count

import requests

from dap_common.api_base import HttpClient
from dap_data.read_data import load_yaml


class dapReviewManageList(HttpClient):
    def __init__(self):
        super().__init__()
        self.httpclient = HttpClient()
        self.data = load_yaml('dap_reviewManageList.yaml')
        self.host = load_yaml('dap_host.yaml')
        self.token = load_yaml('token.yaml')
        self.post_headers = self.token['post_header']
        self.get_headers = self.token['get_header']

    def approve_page(self):
        approvepage_url = self.host['host'] + self.data['approvepage_url']
        approvepage_json = self.data['approvepage_json']
        approvepage_api = self.httpclient.post(approvepage_url, headers=self.post_headers, json=approvepage_json)

        data = approvepage_api.json()['datas']
        return data


    def approve(self):
        data = self.approve_page()
        for index in range(len(data)):
            if data[index]['wfStatus'] == '0':
                approve_url = self.host['host'] + self.data['approve_url']+str(data[index]['id'])
                approve_json = self.data['approve_json']
                http = requests.session()
                approve_api = http.put(approve_url,headers=self.post_headers,json=approve_json,verify=False)
                print(approve_api.status_code)


if __name__ == '__main__':
    approve = dapReviewManageList()
    approve.approve_page()
    approve.approve()
