from dap_common.api_base import HttpClient
from dap_data.read_data import load_yaml


class dapDataFieldList(HttpClient):
    def __init__(self):
        super().__init__()
        self.httpclient = HttpClient()
        self.data = load_yaml('dap_dataFieldList.yaml')
        self.host = load_yaml('dap_host.yaml')
        self.token = load_yaml('token.yaml')
        self.post_headers = self.token['post_header']
        self.get_headers = self.token['get_header']


    def add_dataField(self):
        """新增数据域"""
        adddataField_url = self.host['host'] + self.data['adddataField_url']
        domainNameCn = self.data['adddataField_json']['domainNameCn']
        i = 0
        while i <= max(range(len(domainNameCn))):
            adddataField_json = self.data['adddataField_json']
            self.data['adddataField_json']['domainNameCn'] = domainNameCn[i]
            adddataField_api = self.httpclient.post(adddataField_url, headers=self.post_headers, json=adddataField_json)
            i += 1
            print(adddataField_api.status_code)


    def domain_page(self):
        """"""
