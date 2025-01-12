from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """
    Базовая схема.
    """

    model_config = ConfigDict(
        extra='ignore',  # Игнорирование любых дополнительных атрибутов
        alias_generator=to_camel,  # Преобразование строк из snake_case в camelCase
        populate_by_name=True,  # Поля с псевдонимами могут быть заполнены по имени, указанному в модели
        from_attributes=True,  # При создании моделей выполняется поиск по атрибутам объектов Python
    )
