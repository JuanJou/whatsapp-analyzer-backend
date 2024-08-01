from .base_model import DBModel
from pydantic import BaseModel

class FileData(BaseModel):
    file_id: str
    user_id: int

class File(DBModel):
    table: str = "files"

    @staticmethod
    def write(data: FileData):
        super(File, File).write(data)

