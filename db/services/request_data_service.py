from typing import Optional

from classes.request_data import RequestData
from db.app_database import create_db_and_tables
from db.classes.request_data_class import RequestDataClass
from db.models.request_data_model import RequestDataCreate, RequestDataRead


class RequestDataService:

    @classmethod
    def save(cls, session_id, data: RequestData):
        # print(session_id, data)
        # print(f'data.provider={data.provider}')
        rdata = RequestDataCreate(
            provider=data.provider,
            recipient=data.recipient,
            car=data.car,
            gosnomer = data.gosnomer,
            botanical_variety=data.botanical_variety,
            declared_volume=data.declared_volume,
            total_count=data.total_count,
            large_caliber=data.large_caliber,
            medium_caliber=data.medium_caliber,
            small_caliber=data.small_caliber,
            damage=data.damage,
            phytophthora=data.phytophthora,
            spondylocladium_atrovirens=data.spondylocladium_atrovirens,
            growth_cracks=data.growth_cracks,
            operator_id=data.operator_id,
            operator_surname=data.operator_surname,
            operator_name=data.operator_name,
            operator_patronymic=data.operator_patronymic,
            configuration=data.configuration,
            start_date=data.start_date,
            start_time=data.start_time,
            end_date=data.end_date,
            end_time=data.end_time,
            SessionId=session_id
        )
        RequestDataClass().create(rdata)

    @classmethod
    def get(cls, session_id) -> Optional[RequestData]:
        rdata = RequestDataClass().get(session_id)
        # print(f'RD Service rdata={rdata}')
        if rdata is not None:
            data = RequestData()
            data.provider = rdata.provider
            data.recipient = rdata.recipient
            data.car = rdata.car
            data.gosnomer = rdata.gosnomer
            data.botanical_variety = rdata.botanical_variety
            data.declared_volume = rdata.declared_volume
            data.total_count = rdata.total_count
            data.large_caliber = rdata.large_caliber
            data.medium_caliber = rdata.medium_caliber
            data.small_caliber = rdata.small_caliber
            data.damage = rdata.damage
            data.phytophthora = rdata.phytophthora
            data.spondylocladium_atrovirens = rdata.spondylocladium_atrovirens
            data.growth_cracks = rdata.growth_cracks
            data.operator_id = rdata.operator_id
            data.operator_surname = rdata.operator_surname
            data.operator_name = rdata.operator_name
            data.operator_patronymic = rdata.operator_patronymic
            data.configuration = rdata.configuration
            data.start_date = rdata.start_date
            data.start_time = rdata.start_time
            data.end_date = rdata.end_date
            data.end_time = rdata.end_time
            return data
        else:
            return None

if __name__ == "__main__":
    create_db_and_tables()
    # RequestDataService().save('5b7489c2e00a4303a2383c1f2b06e9f0', RequestData())
    RequestDataService().get('5b7489c2e00a4303a2383c1f2b06e9f0')