import requests

from classes.request_data import RequestData


class HttpRequest():
    # def __init__(self):


    def send_request(self, data):
        try:
            # print(f'http data={data}')
            my_headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyZWNmNjhlOWMyZjlmNzJiMGQ5ODlkZCIsIm5iZiI6MTY1OTY5NjgzNSwiZXhwIjoyMTIzMjMyODM1LCJpc3MiOiJNeUF1dGhTZXJ2ZXIiLCJhdWQiOiJNeUF1dGhTZXJ2ZXIifQ.RDvIfJ8qEXqh-pEozX0hzAHhsjMfNMQgQoB13gAq_Kg'}
            response = requests.post('http://erp.bk-nt.ru/api/analysis/create', json=data,  headers=my_headers)
            # print(f'response={response}')
            return True
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
