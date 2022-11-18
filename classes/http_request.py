from typing import Optional

import requests

from classes.request_data import RequestData


class HttpRequest():

    def get_point(self, pinpoint: str) -> Optional[str]:
        try:
            response = requests.get(f'http://erp.bk-nt.ru/api/point/pair/{pinpoint}')
            print(response.status_code)
            if response.status_code == 200:
                r = response.json()
                print(f'response={r}')
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
            response = requests.post('http://erp.bk-nt.ru/api/auth/point/check', headers=my_headers)
            print(response.status_code)
            if response.status_code == 200:
                r = response.json()
                print(f'response={r["users"]}')
                return r["users"]
            else:
                return None
        except Exception as e:
            return None


    def send_request(self, token, data):
        try:
            # print(f'http data={data}')
            my_headers = {'Authorization': f'Bearer {token}'}
            response = requests.post('http://erp.bk-nt.ru/api/analysis/create', json=data,  headers=my_headers)
            print(f'response={response}')
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False






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
