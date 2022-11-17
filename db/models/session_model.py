import uuid
from typing import Optional

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class SessionBase(SQLModel):
    SessionSuccess: bool = Field(default=False, index=False)

class SessionCreate(SessionBase):
    pass

class SessionUpdate(SessionBase):
    SessionId: Optional[UUID4]

class SessionRead(SessionUpdate):
    pass

class SessionDb(SessionBase, table=True):
    __tablename__ = 'session'
    SessionId: Optional[UUID4] = Field(default_factory=uuid.uuid4, primary_key=True)