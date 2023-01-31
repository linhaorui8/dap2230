from bs4 import BeautifulSoup
from dap_common.api_base import HttpClient
from dap_data.read_data import load_yaml, write_yaml


class SmsLogin(HttpClient):
    def __init__(self):
        super().__init__()
        self.httpclient = HttpClient()
        self.login = load_yaml('login2.yaml')

    def webkit_login(self):
        try:
            login_data = self.login['login_data']
            login_url = self.login['login_url']
            login_headers = self.login['headers']
            login_get = self.httpclient.get(login_url['url'],headers=login_headers)
            html_execution = BeautifulSoup(login_get.content, 'html.parser')
            execution = html_execution.findAll('input')[3].get('value')
            # print(execution)
            login_data['execution'] = execution
            login_success = self.httpclient.post(login_url['url'], data=login_data, headers=login_headers
                                                 , allow_redirects=False)
            # print(login_success.status_code)
            login_token = self.httpclient.get(login_success.headers['Location'], headers=login_headers,allow_redirects=False)
            print(login_token.url)
            print(login_token.request.headers)
            request_cookies = login_token.cookies.get_dict()
            print(request_cookies)
            # print(login_token.headers)
            get_cookies = 'JSESSIONID={0}'.format(request_cookies['JSESSIONID'])
            # print(get_cookies)
            csrf_token = self.httpclient.get(login_url['get_token'])
            csrf_token_content = csrf_token.content
            # print(csrf_token)
            html_execution = BeautifulSoup(csrf_token_content, 'html.parser')
            csrf_token1 = html_execution.find('input').get('value')
            # print(csrf_token1)
            header = {"get_header": {'X-CSRF-TOKEN': csrf_token1, 'Cookie': get_cookies},
                      "post_header": {'X-CSRF-TOKEN': csrf_token1, 'Cookie': get_cookies,
                                      'Content-Type': 'application/json;'}}

            write_yaml(header)
        except Exception as e:
            raise Exception('登录异常%s'%repr(e))



if __name__ == '__main__':
    SmsLogin().webkit_login()

    # url='https://172.16.2.104:8443/back/schedule/common/stat/statDataToday'
    # session=requests.session()
    # # print(session.get(url,headers=get_headers,verify=False).text)
    # url2='https://172.16.2.104:8443/module-common/home'
    # csrf_token=session.get(url2,headers=get_headers,verify=False).content
    # print(csrf_token)
    # html_execution = BeautifulSoup(csrf_token, 'html.parser')
    # csrf_token1 = html_execution.find('input').get('value')
    # print(csrf_token1)
