from .base_model import DBModel
from pydantic import BaseModel

class UserData(BaseModel):
    user_name: str
    hash_password: str

class User(DBModel):
    table: str = "users"

    @staticmethod
    def write(data: UserData):
        super(User, User).write(data)

