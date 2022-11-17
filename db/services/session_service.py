from pydantic import UUID4

from db.app_database import create_db_and_tables
from db.classes.session_class import SessionClass


class SessionService:
    @classmethod
    def count_sessions(cls) -> int:
        sessions = SessionClass().get()
        return len(sessions)

    @classmethod
    def get_sessions(cls):
        sessions = SessionClass().get()
        return sessions

    @classmethod
    def new_session_id(cls) -> UUID4:
        new_session = SessionClass().create()
        return new_session.SessionId

    @classmethod
    def update_session(cls, session_id):
        SessionClass().update(session_id=session_id)

if __name__ == "__main__":
    create_db_and_tables()
    # new_id = SessionService.new_session_id()
    # print(f'new_id={new_id}')
    SessionService().update_session('bae9622027ea4340baed93387d693fc7')
