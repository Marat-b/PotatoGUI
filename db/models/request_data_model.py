import uuid
from typing import Optional

from pydantic import UUID4
from sqlalchemy import table
from sqlmodel import Field, SQLModel


class RequestDataBase(SQLModel):
    provider: str = Field(default='', index=False)
    recipient: str = Field(default='', index=False)
    car: str = Field(default='', index=False)
    gosnomer: str = Field(default='', index=False)
    botanical_variety: str = Field(default='', index=False)
    declared_volume: str = Field(default='', index=False)
    total_count: str = Field(default='', index=False)
    large_caliber: str = Field(default='', index=False)
    medium_caliber: str = Field(default='', index=False)
    small_caliber: str = Field(default='', index=False)
    damage: str = Field(default='', index=False)
    phytophthora: str = Field(default='', index=False)
    spondylocladium_atrovirens: str = Field(default='', index=False)
    growth_cracks: str = Field(default='', index=False)
    operator_id: str = Field(default='', index=False)
    operator_surname: str = Field(default='', index=False)
    operator_name: str = Field(default='', index=False)
    operator_patronymic: str = Field(default='', index=False)
    configuration: str = Field(default='', index=False)
    start_date: str = Field(default='', index=False)
    start_time: str = Field(default='', index=False)
    end_date: str = Field(default='', index=False)
    end_time: str = Field(default='', index=False)
    SessionId: UUID4 = Field(index=False)

class RequestDataCreate(RequestDataBase):
    pass

class RequestDataUpdate(RequestDataBase):
    RequestDataId: Optional[UUID4]

class RequestDataRead(RequestDataUpdate):
    pass

class RequestDataDb(RequestDataBase, table=True):
    __tablename__ = 'request_data'
    RequestDataId: Optional[UUID4] =  Field(default_factory=uuid.uuid4, primary_key=True)
