import datetime
import time
import requests


class HttpRequest():
    def __init__(self):
        self._data = {
            "settings": {
                "provider": "ООО Полог",
                "recipient": "ООО Низина",
                "car": "КАМАЗ 3215",
                "gosnomer": "У678КР199",
                "botanical_variety": "Поздняя",
                "declared_volume": "10 тонн",
                "total_count": "0",
                "large_caliber": "0",
                "medium_caliber": "0",
                "small_caliber": "0",
                "damage": "0",
                "phytophthora": "0",
                "spondylocladium_atrovirens": "0",
                "growth_cracks": "0",
                "null": "23"
            },
            "operator": {
                "id": "62ecf3f89c2f9f72b0d989d2",
                "surname": "фон Бабаян",
                "name": "Карл-Густав",
                "patronymic": "Ахмед оглы"
            },
            "configuration": "62eb5881f54a8809ca9c8db9",
            "start_date": "2022-08-05",
            "end_date": "2022-08-05",
            "start_time": "13:10",
            "end_time": "14:00"
        }

    def send_request(self):
        print(f'http data={self._data}')
        my_headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyZWNmNjhlOWMyZjlmNzJiMGQ5ODlkZCIsIm5iZiI6MTY1OTY5NjgzNSwiZXhwIjoyMTIzMjMyODM1LCJpc3MiOiJNeUF1dGhTZXJ2ZXIiLCJhdWQiOiJNeUF1dGhTZXJ2ZXIifQ.RDvIfJ8qEXqh-pEozX0hzAHhsjMfNMQgQoB13gAq_Kg'}
        response = requests.post('http://erp.bk-nt.ru/api/analysis/create', json=self._data,  headers=my_headers)
        print(f'response={response}')

    @property
    def data(self):
        return self._data

    def provider(self, item):
        self._data['settings']['provider'] = item

    def car(self, item):
        self._data['settings']['car'] = item

    def botanical_variety(self, item):
        self._data['settings']['botanical_variety'] = item

    def declared_volume(self, item):
        self._data['settings']['declared_volume'] = item

    def total_count(self, item):
        self._data['settings']['total_count'] = item

    def large_caliber(self, item):
        self._data['settings']['large_caliber'] = item

    def medium_caliber(self, item):
        self._data['settings']['medium_caliber'] = item

    def small_caliber(self, item):
        self._data['settings']['small_caliber'] = item

    def phytophthora(self, item):
        self._data['settings']['phytophthora'] = item

    ################ configuration ############################

    def start_date(self, item=str(datetime.date.today())):
        self._data['start_date'] = item

    def start_time(self, item=time.strftime('%H:%M', time.localtime())):
        self._data['start_time'] = item

    def end_date(self, item=str(datetime.date.today())):
        self._data['end_date'] = item

    def end_time(self, item=time.strftime('%H:%M', time.localtime())):
        self._data['end_time'] = item




if __name__ == '__main__':
    hr = HttpRequest()
    hr.total_count = '90909'
    hr.start_date()
    hr.start_time()
    hr.end_date()
    hr.end_time()
    print(hr.data)
    hr.send_request()
