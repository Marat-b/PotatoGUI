from typing import List

from sqlmodel import Session, select

from db.app_database import create_db_and_tables, get_engine, get_session
from db.models.session_model import SessionCreate, SessionDb, SessionRead


class SessionClass:
    # def __init__(self, engine=get_engine()):
    #     self.engine = engine
    def __init__(self, session=get_session()):
        self.session = session

    def create(self) -> SessionRead:
        new_session = SessionDb.from_orm(SessionCreate())
        self.session.add(new_session)
        self.session.commit()
        self.session.refresh(new_session)
        # with Session(self.engine) as s:
        #     s.add(new_session)
        #     s.commit()
        #     s.refresh(new_session)
        # new_session = SessionDb.from_orm(SessionCreate())
        return new_session

    def get(self) -> List[SessionRead]:
        condition_statement = select(SessionDb).where(SessionDb.SessionSuccess==False)
        result = self.session.exec(condition_statement)
        return result.all()

    def update(self, session_id) -> bool:
        condition_statement = select(SessionDb).where(SessionDb.SessionId == session_id)
        session_obj = self.session.exec(condition_statement).first()
        if session_obj is not None:
            session_obj.SessionSuccess=True
            self.session.add(session_obj)
            self.session.commit()
            return True
        else:
            return False

if __name__ == "__main__":
    # engine = create_engine("sqlite:///database.db")
    create_db_and_tables()
    # s = SessionClass().create()
    # print(f'id={s.SessionId}')
    SessionClass().update('bae9622027ea4340baed93387d693fc7')