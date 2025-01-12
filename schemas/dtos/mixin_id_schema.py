from typing import Optional

from pydantic import Field

from .base_schema import BaseSchema


class MixinIdSchema(BaseSchema):
    """
    Миксина для добавления поля id к схеме.
    """

    id: Optional[int] = Field(ge=0, description='ID сущности', init_var=True, kw_only=True, examples=[0], default=0)
