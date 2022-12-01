from typing import Optional

from db.classes.option_class import OptionClass
from db.models.option_model import OptionRead


class OptionService:
    @classmethod
    def get_option(cls, name) -> Optional[OptionRead]:
        option = OptionClass().get(name)
        return option


    @classmethod
    def update_option(cls, name, value):
        OptionClass().update(name=name, value=value)
