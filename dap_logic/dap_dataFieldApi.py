from dap_common.api_base import HttpClient
from dap_data.read_data import load_yaml
import allure


@allure.feature('数据源管理Api')
class dapDataFieldList(HttpClient):
    def __init__(self):
        super().__init__()
        self.httpclient = HttpClient()
        self.data = load_yaml('dap_dataFieldList.yaml')
        self.host = load_yaml('dap_host.yaml')
        self.token = load_yaml('token.yaml')
        self.post_headers = self.token['post_header']
        self.get_headers = self.token['get_header']

    @allure.title('新增数据域接口用例')
    def add_dataField(self):
        """新增数据域接口"""
        adddataField_api = None

        adddataField_url = self.host['host'] + self.data['adddataField_url']
        domainNameCn = self.data['adddataField_json']['domainNameCn']
        i = 0
        while i <= max(range(len(domainNameCn))):
            adddataField_json = self.data['adddataField_json']
            self.data['adddataField_json']['domainNameCn'] = domainNameCn[i]
            adddataField_api = self.httpclient.post(adddataField_url, headers=self.post_headers,
                                                    json=adddataField_json)
            i += 1
        try:
            if adddataField_api.status_code == 200:
                pass
        except Exception as e:
            print('新增数据域接口出错%s' % adddataField_api.text, e)
        else:
            return adddataField_api

    def domain_page1(self):
        """查询数据域列表接口"""
        dataFieldpage_api = None
        try:
            dataFieldpage_url = self.host['host'] + self.data['dataFieldpage_url']
            dataFieldpage_json = self.data['dataFieldpage_json']
            dataFieldpage_api = self.httpclient.post(dataFieldpage_url, headers=self.post_headers,
                                                     json=dataFieldpage_json)
            # print(dataFieldpage_api.json())
            return dataFieldpage_api.json()['datas']
        except Exception as e:
            print('接口异常:%s' % dataFieldpage_api.text, e)

    # def user_page(self):
    #     """查询平台用户id，返回--->列表[]"""
    #     userpage_url = self.host['host'] + self.data['userpage_url']
    #     userpage_api = self.httpclient.post(userpage_url,headers=self.post_headers,json={})
    #     print(userpage_api.json())
    def domain_page2(self, value, get_json):
        global domain_ids
        dataSource_ids = self.datasourcelist()

        dataFieldpage_url = self.host['host'] + self.data['dataFieldpage_url']
        dataFieldpage_json = self.data['dataFieldpage_json']
        dataFieldpage_api = self.httpclient.post(dataFieldpage_url, headers=self.post_headers,
                                                 json=dataFieldpage_json)
        # print(dataFieldpage_api.json())
        try:
            domain_ids = dataFieldpage_api.json()['datas']
        except Exception as e:
            print('error%s' % dataFieldpage_api.text, e)
        else:
            if value == 1:
                for domain_id in range(len(domain_ids) - 1):
                    """拿到数据域的id，排除id=0公共数据域"""
                    if domain_ids[domain_id]['domainNameCn'] == "gauss+mysql":
                        get_json['domainId'] = domain_ids[domain_id]['id']
                        for dt_id in range(len(dataSource_ids)):
                            """判断数据源是gauss，则传入dataSource_id; 物化源是mysql，传入logicSource_id"""
                            if 'gauss' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 1:
                                get_json['dataSourceList'] = [dataSource_ids[dt_id]['id']]
                            if 'mysql' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 2:
                                get_json['logicDatabase'] = dataSource_ids[dt_id]['id']
                                get_json['resultDatabase'] = dataSource_ids[dt_id]['id']
                                get_json['summaryDatabase'] = dataSource_ids[dt_id]['id']
                    if domain_ids[domain_id]['domainNameCn'] == "mysql+gauss":
                        get_json['domainId'] = domain_ids[domain_id]['id']
                        for dt_id in range(len(dataSource_ids)):
                            """判断数据源是mysql，则传入dataSource_id; 物化源是gauss,传入logicSource_id"""
                            if 'mysql' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 1:
                                get_json['dataSourceList'] = [dataSource_ids[dt_id]['id']]
                            if 'gauss' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 2:
                                get_json['logicDatabase'] = dataSource_ids[dt_id]['id']
                                get_json['resultDatabase'] = dataSource_ids[dt_id]['id']
                                get_json['summaryDatabase'] = dataSource_ids[dt_id]['id']
            elif value == 2:
                for domain_id in range(len(domain_ids) - 1):
                    if domain_ids[domain_id]['domainNameCn'] == "mysql+gauss":
                        get_json['domainId'] = domain_ids[domain_id]['id']
                    for dt_id in range(len(dataSource_ids)):
                        """判断数据源是mysql，则传入dataSource_id; 物化源是gauss,传入logicSource_id"""
                        if 'mysql' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 1:
                            get_json['dbId'] = dataSource_ids[dt_id]['id']
                            get_json['srcDbId'] = dataSource_ids[dt_id]['id']
            return value

    def add_userauth(self):
        """添加用户业务域权限"""
        adduserauth_api = None

        id = self.domain_page1()
        index = 0
        while index <= max(range(len(id) - 1)):
            adduserauth_url = self.host['host'] + self.data['adduserauth_url'] + str(id[index]['id'])
            adduserauth_json = self.data['adduserauth_json']
            adduserauth_api = self.post(adduserauth_url, headers=self.post_headers, json=adduserauth_json)
            # print(adduserauth_api.status_code)
            index += 1

        try:
            return adduserauth_api
        except Exception as e:
            print('添加用户业务域权限状态异常:{}'.format(adduserauth_api.text), e)

    def datasourcelist(self):
        """数据源列表接口，返回数据源和物化源"""
        datasourcelist_api = None
        try:
            datasourcelist_url = self.host['host'] + self.data['datasourcelist_url']
            datasourcelist_json = self.data['datasourcelist_json']
            datasourcelist_api = self.post(datasourcelist_url, headers=self.post_headers, json=datasourcelist_json)

            return datasourcelist_api.json()
        except Exception as e:
            print('数据源列表接口error%s' % datasourcelist_api.json(), e)

    def set_domaindb(self):
        """设置数据源：mysql+gauss,gauss+mysql"""
        setdomaindb_api = None
        dataSource_ids = self.datasourcelist()
        setdomaindb_url = self.host['host'] + self.data['setdomaindb_url']
        setdomaindb_json = self.data['setdomaindb_json']
        self.domain_page2(1, setdomaindb_json)
        # for domain_id in range(len(domain_ids) - 1):
        #     """拿到数据域的id，排除id=0公共数据域"""
        #     if domain_ids[domain_id]['domainNameCn'] == "gauss+mysql":
        #         setdomaindb_json['domainId'] = domain_ids[domain_id]['id']
        #         for dt_id in range(len(dataSource_ids)):
        #             """判断数据源是gauss，则传入dataSource_id; 物化源是mysql，传入logicSource_id"""
        #             if 'gauss' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 1:
        #                 setdomaindb_json['dataSourceList'] = [dataSource_ids[dt_id]['id']]
        #             if 'mysql' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 2:
        #                 setdomaindb_json['logicDatabase'] = dataSource_ids[dt_id]['id']
        #                 setdomaindb_json['resultDatabase'] = dataSource_ids[dt_id]['id']
        #                 setdomaindb_json['summaryDatabase'] = dataSource_ids[dt_id]['id']
        #     if domain_ids[domain_id]['domainNameCn'] == "mysql+gauss":
        #         setdomaindb_json['domainId'] = domain_ids[domain_id]['id']
        #         for dt_id in range(len(dataSource_ids)):
        #             """判断数据源是mysql，则传入dataSource_id; 物化源是gauss,传入logicSource_id"""
        #             if 'mysql' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 1:
        #                 setdomaindb_json['dataSourceList'] = [dataSource_ids[dt_id]['id']]
        #             if 'gauss' in dataSource_ids[dt_id]['name'] and dataSource_ids[dt_id]['dbUseType'] == 2:
        #                 setdomaindb_json['logicDatabase'] = dataSource_ids[dt_id]['id']
        #                 setdomaindb_json['resultDatabase'] = dataSource_ids[dt_id]['id']
        #                 setdomaindb_json['summaryDatabase'] = dataSource_ids[dt_id]['id']
        #     print(setdomaindb_json)
        try:
            setdomaindb_api = self.post(setdomaindb_url, headers=self.post_headers, json=setdomaindb_json)
            print(setdomaindb_api.status_code)

        except Exception as e:
            print('设置数据源error%s' % setdomaindb_api.text, e)


if __name__ == '__main__':
    domain = dapDataFieldList()
    domain.add_dataField()
    # print(domain.add_userauth())
  #  domain.set_domaindb()
