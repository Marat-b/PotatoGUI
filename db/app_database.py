from sqlmodel import SQLModel, Session, create_engine

engine = create_engine("sqlite:///db/database.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    pass


def get_session():
    with Session(engine) as session:
        return session

def get_engine():
    return engine