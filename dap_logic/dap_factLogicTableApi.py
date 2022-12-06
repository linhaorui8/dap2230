import random

from dap_common.api_base import HttpClient
from dap_data.read_data import load_yaml
from dap_logic.dap_dimensionApi import dapdimenSionList


class dapfactLogicTable(HttpClient):
    def __init__(self):
        super().__init__()
        self.httpclient = HttpClient()
        self.data = load_yaml('dap_businessdef.yaml')
        self.host = load_yaml('dap_host.yaml')
        self.token = load_yaml('token.yaml')
        self.post_headers = self.token['post_header']
        self.get_headers = self.token['get_header']
