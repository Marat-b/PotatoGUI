from typing import List, Optional

from sqlmodel import  select

from db.app_database import create_db_and_tables,  get_session
from db.models.option_model import OptionCreate, OptionDb, OptionRead


class OptionClass:
    def __init__(self, option=get_session()):
        self.option = option

    def create(self) -> OptionRead:
        new_option = OptionDb.from_orm(OptionCreate())
        self.option.add(new_option)
        self.option.commit()
        self.option.refresh(new_option)
        # with Option(self.engine) as s:
        #     s.add(new_option)
        #     s.commit()
        #     s.refresh(new_option)
        # new_option = OptionDb.from_orm(OptionCreate())
        return new_option

    def get(self, name) -> Optional[OptionRead]:
        condition_statement = select(OptionDb).where(OptionDb.Name == name)
        result = self.option.exec(condition_statement)
        return result.one_or_none()

    def update(self, name, value) -> OptionRead:
        condition_statement = select(OptionDb).where(OptionDb.Name == name)
        option_obj = self.option.exec(condition_statement).first()
        if option_obj is not None:
            option_obj.Value=value
            self.option.add(option_obj)
            self.option.commit()
            self.option.refresh(option_obj)
        else:
            option_obj = OptionDb.from_orm(OptionCreate())
            option_obj.Name = name
            option_obj.Value = value
            self.option.add(option_obj)
            self.option.commit()
            self.option.refresh(option_obj)
        return option_obj

if __name__ == "__main__":
    # engine = create_engine("sqlite:///database.db")
    create_db_and_tables()
    # s = OptionClass().create()
    # print(f'id={s.OptionId}')
    OptionClass().update('bae9622027ea4340baed93387d693fc7')