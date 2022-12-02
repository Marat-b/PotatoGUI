import json
from typing import Optional

import requests

from classes.request_data import RequestData


class HttpRequest():
    def __init__(self, ip_address='127.0.0.1', port=None):
        self.ip_address = ip_address
        self.port = port

    def __call__(self,ip_address='127.0.0.1', port=None):
        self.ip_address = ip_address
        self.port = port

    def check_password(self, login, password) -> bool:
        payload = {'login': login, 'password': password}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        print(f'payload={payload}')
        response = requests.post('http://176.99.12.88:8080/api/auth/login',
                                 data=json.dumps(payload), headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            r = response.json()
            # print(f'response={r}')
            if r["error"] == False:
                return True
            else:
                return False


    def get_point(self, pinpoint: str) -> Optional[str]:
        try:
            response = requests.get(f'http://{self.ip_address}/api/point/pair/{pinpoint}')
            print(response.status_code)
            if response.status_code == 200:
                r = response.json()
                # print(f'response={r}')
                if r["error"] == False:
                    return r["data"]
                else:
                    return None
            else:
                return None
        except Exception as e:
            return None

    def get_check(self, token):
        try:
            my_headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(f'http://{self.ip_address}/api/auth/point/check', headers=my_headers)
            print(response.status_code)
            if response.status_code == 200:
                r = response.json()
                # print(f'response={r}')
                return r["users"]
            else:
                print(f'Status code={response.status_code}')
                return None
        except Exception as e:
            print(f'Error is {e}')
            return None


    def send_request(self, token, data):
        try:
            # print(f'http data={data}')
            my_headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(f'http://{self.ip_address}/api/analysis/create', json=data,  headers=my_headers)
            # print(f'response={response}')
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_analisis_list(self, token, data):
        try:
            # print(f'http data={data}')
            my_headers = {'Authorization': f'Bearer {token}', 'Content-type': 'application/json', 'Accept': 'text/plain'}
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = requests.post(f'http://{self.ip_address}/api/analysis/list',
                                     data=json.dumps(data), headers=my_headers)
            # print(f'response={response}')
            if response.status_code == 200:
                r = response.json()
                return r
            else:
                print(f'Status code={response.status_code}')
                return None
        except Exception as e:
            print(f'Error is {e}')
            return None







if __name__ == '__main__':
    hr = HttpRequest()
    # hr.total_count = '90909'
    # hr.start_date()
    # hr.start_time()
    # hr.end_date()
    # hr.end_time()
    # print(hr.data)
    ret = hr.send_request(RequestData().data)
    print(ret)
