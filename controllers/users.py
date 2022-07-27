from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users", "general"],
    responses={404: {"description": "Not found"}}
)


class User(BaseModel):
    name: str
    lastname: str

@router.post("/save/")
def save(user: User):
    print("USER", user)
    return 



