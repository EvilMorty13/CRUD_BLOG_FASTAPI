from pydantic import BaseModel, ConfigDict, EmailStr
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return handler(core_schema) | {"type": "string", "format": "objectid"}

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return handler.generate_schema(str)

class User(BaseModel):
    id: PyObjectId | None = None
    username: str
    email: EmailStr
    hashed_password: str

    model_config = ConfigDict(arbitrary_types_allowed=True)
