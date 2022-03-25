from pydantic import BaseModel, validator, constr
from datetime import datetime


class User(BaseModel):
    id: int = None
    username: str
    name: str
    lastname: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def object_parse(cls, item):
        item.__dict__.pop('_sa_instance_state', None)
        return cls.parse_obj(item.__dict__)


class UserIn(BaseModel):
    username: str
    name: str
    lastname: str
    password: constr(min_length=8)
    password2: str
    _created_at: datetime
    _updated_at: datetime

    @validator("password2")
    def password_validate(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v
