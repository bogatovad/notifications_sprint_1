import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONBaseModel(BaseModel):
    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps
