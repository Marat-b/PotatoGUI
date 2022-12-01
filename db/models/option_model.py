import uuid
from typing import Optional

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class OptionBase(SQLModel):
    Name: str = Field(default='', index=True)
    Value: str = Field(default='', index=False)

class OptionCreate(OptionBase):
    pass

class OptionUpdate(OptionBase):
    OptionId:  Optional[UUID4]

class OptionRead(OptionUpdate):
    pass

class OptionDb(OptionBase, table=True):
    __tablename__ = 'options'
    OptionId: Optional[UUID4] = Field(default_factory=uuid.uuid4, primary_key=True)