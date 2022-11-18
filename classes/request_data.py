import time
import datetime


class RequestData:
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
                "id": "",
                "surname": "",
                "name": "",
                "patronymic": ""
            },
            "configuration": "62eb5881f54a8809ca9c8db9",
            "start_date": "2022-08-05",
            "end_date": "2022-08-05",
            "start_time": "13:10",
            "end_time": "14:00"
        }

    @property
    def data(self):
        return self._data

    @property
    def provider(self):
        return self._data['settings']['provider']

    @provider.setter
    def provider(self, item):
        self._data['settings']['provider'] = item

    @property
    def recipient(self):
        return self._data['settings']['recipient']

    @recipient.setter
    def recipient(self, item):
        self._data['settings']['recipient'] = item

    @property
    def car(self):
        return self._data['settings']['car']

    @car.setter
    def car(self, item):
        self._data['settings']['car'] = item

    @property
    def gosnomer(self):
        return self._data['settings']['gosnomer']

    @gosnomer.setter
    def gosnomer(self, item):
        self._data['settings']['gosnomer'] = item

    @property
    def botanical_variety(self):
        return self._data['settings']['botanical_variety']

    @botanical_variety.setter
    def botanical_variety(self, item):
        self._data['settings']['botanical_variety'] = item

    @property
    def declared_volume(self):
        return self._data['settings']['declared_volume']

    @declared_volume.setter
    def declared_volume(self, item):
        self._data['settings']['declared_volume'] = item

    @property
    def total_count(self):
        return self._data['settings']['total_count']

    @total_count.setter
    def total_count(self, item):
        self._data['settings']['total_count'] = item

    @property
    def large_caliber(self):
        return self._data['settings']['large_caliber']

    @large_caliber.setter
    def large_caliber(self, item):
        self._data['settings']['large_caliber'] = item

    @property
    def medium_caliber(self):
        return self._data['settings']['medium_caliber']

    @medium_caliber.setter
    def medium_caliber(self, item):
        self._data['settings']['medium_caliber'] = item

    @property
    def small_caliber(self):
        return self._data['settings']['small_caliber']

    @small_caliber.setter
    def small_caliber(self, item):
        self._data['settings']['small_caliber'] = item

    @property
    def damage(self):
        return self._data['settings']['damage']

    @damage.setter
    def damage(self, item):
        self._data['settings']['damage'] = item

    @property
    def phytophthora(self):
        return self._data['settings']['phytophthora']

    @phytophthora.setter
    def phytophthora(self, item):
        self._data['settings']['phytophthora'] = item

    @property
    def spondylocladium_atrovirens(self):
        return self._data['settings']['spondylocladium_atrovirens']

    @spondylocladium_atrovirens.setter
    def spondylocladium_atrovirens(self, item):
        self._data['settings']['spondylocladium_atrovirens'] = item

    @property
    def growth_cracks(self):
        return self._data['settings']['growth_cracks']

    @growth_cracks.setter
    def growth_cracks(self, item):
        self._data['settings']['growth_cracks'] = item

    ############### operator #################################
    @property
    def operator_id(self):
        return self._data['operator']['id']

    @operator_id.setter
    def operator_id(self, item):
        self._data['operator']['id'] = item

    @property
    def operator_surname(self):
        return self._data['operator']['surname']

    @operator_surname.setter
    def operator_surname(self, item):
        self._data['operator']['surname'] = item

    @property
    def operator_name(self):
        return self._data['operator']['name']

    @operator_name.setter
    def operator_name(self, item):
        self._data['operator']['name'] = item

    @property
    def operator_patronymic(self):
        return self._data['operator']['patronymic']

    @operator_patronymic.setter
    def operator_patronymic(self, item):
        self._data['operator']['patronymic'] = item

    ################ configuration ############################

    @property
    def configuration(self):
        return self._data['configuration']

    @configuration.setter
    def configuration(self, item):
        self._data['configuration'] = item

    @property
    def start_date(self):
        return self._data['start_date']

    @start_date.setter
    def start_date(self, item):
        self._data['start_date'] = item

    # def start_time(self, item=time.strftime('%H:%M', time.localtime())):
    #     self._data['start_time'] = item
    @property
    def start_time(self):
        return self._data['start_time']

    @start_time.setter
    def start_time(self, item):
        self._data['start_time'] = item

    @property
    def end_date(self):
        return self._data['end_date']

    @end_date.setter
    def end_date(self, item):
        # =str(datetime.date.today())
        self._data['end_date'] = item

    @property
    def end_time(self):
        return self._data['end_time']

    @end_time.setter
    def end_time(self, item):
        self._data['end_time'] = item