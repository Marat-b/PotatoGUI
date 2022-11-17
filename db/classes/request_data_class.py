from typing import Optional

from sqlmodel import select

from db.app_database import get_session
from db.models.request_data_model import RequestDataCreate, RequestDataDb, RequestDataRead


class RequestDataClass:
    def __init__(self, session=get_session()):
        self.session = session

    def create(self, rdata: RequestDataCreate) -> None:
        # rdata = RequestDataCreate()
        # rdata.SessionId = session_id
        new_data = RequestDataDb.from_orm(rdata)
        self.session.add(new_data)
        self.session.commit()

    def get(self, session_id) -> Optional[RequestDataRead]:
        condition_statement = select(RequestDataDb).where(RequestDataDb.SessionId == session_id)
        record = self.session.exec(condition_statement).first()
        return record

# if __name__ == "__main__":
#     create_db_and_tables()
#     record = RequestDataClass.get()