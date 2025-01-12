from typing import Any

from pydantic import BaseModel


class BaseSchemaForEvent(BaseModel):
    queue: str = ''
    function: Any = None
    depends_on_exchange: str = ''
