from dap_common.api_base import HttpClient
from dap_data.read_data import load_yaml


class dapDataSourceList(HttpClient):
    def __init__(self):
        super().__init__()
        self.httpclient = HttpClient()
        self.data = load_yaml('dap_dataSourceList.yaml')
        self.host = load_yaml('dap_host.yaml')
        self.token = load_yaml('token.yaml')
        self.post_headers = self.token['post_header']
        self.get_headers = self.token['get_header']

    def sources_list(self):
        """查询数据源接口"""
        try:
            choice_sources_url = self.host['host'] + self.data['choice_sources_url']
            choice_sources_api = self.httpclient.get(choice_sources_url, headers=self.get_headers)
            source_ids = choice_sources_api.json()
            return source_ids
        except Exception as e:
            print('接口请求异常',e)

    def add_datasource(self):
        """新增数据源"""
        source_ids = self.sources_list()
        addsource_url = self.host['host'] + self.data['addsource_url']
        addsource_json = self.data['addsource_json']
        ids = 0
        while ids <= max(range(len(source_ids))):
            addsource_json['srcId'] = source_ids[ids]['id']
            addsource_api = self.httpclient.post(addsource_url, headers=self.post_headers, json=addsource_json)
            ids += 1
            print(addsource_api.status_code)

    def add_logicalsource(self):
        """新增物化源"""
        addlogicalsource_url = self.host['host'] + self.data['addlogicalsource_url']
        addlogicalsource_json = self.data['addlogicalsource_json']
        ids = 0
        source_ids = self.sources_list()
        while ids <= max(range(len(source_ids))):
            addlogicalsource_json['srcId'] = source_ids[ids]['id']
            addsource_api = self.httpclient.post(addlogicalsource_url, headers=self.post_headers,
                                                 json=addlogicalsource_json)
            ids += 1
            print(addsource_api.status_code)




if __name__ == '__main__':
    source = dapDataSourceList()
    print(source.sources_list())
    source.add_datasource()
    source.add_logicalsource()

