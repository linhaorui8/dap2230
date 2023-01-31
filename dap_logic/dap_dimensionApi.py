import random

from dap_common.api_base import HttpClient
from dap_data.read_data import load_yaml
from dap_logic.dap_dataFieldApi import dapDataFieldList


class dapdimenSionList(HttpClient):

    def __init__(self):
        super().__init__()
        self.httpclient = HttpClient()
        self.data = load_yaml('dap_businessdef.yaml')
        self.host = load_yaml('dap_host.yaml')
        self.token = load_yaml('token.yaml')
        self.post_headers = self.token['post_header']
        self.get_headers = self.token['get_header']

    def add_businessdef(self):
        """新增业务过程API"""
        businessdef_api = None
        try:
            domain_id = dapDataFieldList().domain_page1()
            for id in range(len(domain_id)):
                if domain_id[id]['domainNameCn'] == 'mysql+gauss' and domain_id[id]['domainNameCn'] != '公共数据域':
                    businessdef_url = self.host['host'] + self.data['businessdef_url']
                    businessdef_json = self.data['businessdef_json']
                    domain_id[id]['id'] = businessdef_json['domainId']
                    businessdef_api = self.httpclient.post(businessdef_url, headers=self.post_headers,
                                                           json=businessdef_json)
        except Exception as e:
            print('调用接口异常%s' % businessdef_api.json(), e)

    def businessdef_page(self):
        """返回业务过程id"""
        businessdefpage_api = None
        try:
            businessdefpage_url = self.host['host'] + self.data['businessdefpage_url']
            businessdefpage_json = self.data['businessdefpage_json']
            businessdefpage_api = self.httpclient.post(businessdefpage_url, headers=self.post_headers,
                                                       json=businessdefpage_json)
            return businessdefpage_api.json()['id']
        except Exception as e:
            print('调用接口异常%s' % businessdefpage_api.text, e)

    def add_dimsrc(self):
        """返回维度的pkColid"""
        addsrc_api = None
        try:

            # dataSource_ids = dapDataFieldList().datasourcelist()
            addsrc_url = self.host['host'] + self.data['addsrc_url']
            addsrc_json = self.data['addsrc_json']
            dapDataFieldList().domain_page2(2,addsrc_json)
            # for domain_id in range(len(domain_ids) - 1):
            #     if domain_ids[domain_id]['domainNameCn'] == "mysql+gauss":
            #         addsrc_json['domainId'] = domain_ids[domain_id]['id']
            #     for dt_id in range(len(dataSource_ids)):
            #         """判断数据源是mysql，则传入dataSource_id; 物化源是gauss,传入logicSource_id"""
            #         if 'mysql' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 1:
            #             addsrc_json['dbId'] = dataSource_ids[dt_id]['id']
            #             addsrc_json['srcDbId'] = dataSource_ids[dt_id]['id']
            addsrc_api = self.post(addsrc_url, headers=self.post_headers, json=addsrc_json)
            return addsrc_api.json()['id']
        except Exception as e:
            print('调用接口异常%s' % addsrc_api.text, e)

    def add_dimdef(self):
        """新增普通维度"""
        adddimdef_api = None
        try:
            domain_ids = dapDataFieldList().domain_page1()
            dataSource_ids = dapDataFieldList().datasourcelist()
            pkColid = self.add_dimsrc()
            adddimdef_url = self.host['host'] + self.data['adddimdef_url']
            adddimdef_json = self.data['adddimdef_json']
            adddimdef_json['pkColId'] = pkColid
            adddimdef_json['tabName'] = adddimdef_json['tabName'] + str(random.randint(1, 50))
            for domain_id in range(len(domain_ids) - 1):
                if domain_ids[domain_id]['domainNameCn'] == "mysql+gauss":
                    adddimdef_json['domainId'] = domain_ids[domain_id]['id']
                for dt_id in range(len(dataSource_ids)):
                    """判断数据源是mysql，则传入dataSource_id; 物化源是gauss,传入logicSource_id"""
                    if 'mysql' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 1:
                        adddimdef_json['dbId'] = dataSource_ids[dt_id]['id']
                        adddimdef_json['srcDbId'] = dataSource_ids[dt_id]['id']
            adddimdef_api = self.post(adddimdef_url, headers=self.post_headers, json=adddimdef_json)

        except Exception as e:
            print('调用接口异常%s' % adddimdef_api.text, e)


if __name__ == '__main__':
    dim = dapdimenSionList()
    print(dim.add_businessdef().text)
   # dim.businessdef_page()
    # dim.add_src()
   # dim.add_dimsrc()
