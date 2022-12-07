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

    def check_password(self, login, password) -> Optional[dict]:
        payload = {'login': login, 'password': password}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # print(f'payload={payload}')
        response = requests.post(f'http://{self.ip_address}/api/auth/login', # 176.99.12.88:8080
                                 data=json.dumps(payload), headers=headers)
        # print(response.status_code)
        if response.status_code == 200:
            r = response.json()
            # print(f'response={r}')
            if r["error"] == False:
                return r
            else:
                return None


    def get_point(self, pinpoint: str) -> Optional[str]:
        try:
            response = requests.get(f'http://{self.ip_address}/api/point/pair/{pinpoint}')
            # print(response.status_code)
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
            # print(response.status_code)
            if response.status_code == 200:
                r = response.json()
                # print(f'response={r}')
                return r
            else:
                # print(f'Status code={response.status_code}')
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

    def get_analisis_list(self, token, current_client, data):
        try:
            # print(f'get_analisis_list token={token}')
            res = requests.post(
                f'http://{self.ip_address}/api/auth/check',
                data=json.dumps({"client": current_client, "path": "/client/analysis/list"}),
                # json={"client": "62ecf3c29c2f9f72b0d989ce", "path": "/client/analysis/list"},
                headers={"Authorization": f"Bearer {token}", "Content-type": "application/json", "Accept":
                    "text/plain"}
            )
            print(f'resp={res}')
            if res.status_code == 200:
                r = res.json()
                check_token = r['token']
                print(f'2 check_torken={check_token}')
                my_headers = {'Authorization': f'Bearer {check_token}', 'Content-type': 'application/json', 'Accept':
                    'text/plain'}
                # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                response = requests.post(f'http://{self.ip_address}/api/analysis/list',
                                         data=json.dumps(data), headers=my_headers)
                print(f'get_analisis_list response={response}')
                if response.status_code == 200:
                    r = response.json()
                    print(f'get_analisis_list r={r}')
                    return r
                else:
                    # print(f'Status code={response.status_code}')
                    return None
            else:
                return None
        except Exception as e:
            print(f'Error is {e}')
            return None

    def get_check_dashboard(self, token, current_client_id):
        try:
            # print(f'current_client_id={current_client_id}')
            res = requests.post(
                f'http://{self.ip_address}/api/auth/check',
                data=json.dumps({"client": current_client_id, "path": "/client/dashboard"}),
                headers={
                    "Authorization": f"Bearer {token}", "Content-type": "application/json", "Accept":
                        "text/plain"
                }
            )
            # print(f'get_check_dashboard res={res}')
            if res.status_code == 200:
                r = res.json()
                print(f'get_check_dashboard r={r["client"]}')
                return r['client']['legal']['name']
            else:
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
