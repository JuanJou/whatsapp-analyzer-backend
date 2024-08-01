from typing import Annotated
from fastapi import APIRouter, UploadFile, Depends, Query, Security
from services.user import get_user, save_user
from db.models import UserData


router = APIRouter(prefix="/user", tags=["users"])

@router.get("")
def parse(user_id: Annotated[str, "User id to retreive"]):
    user = get_user(user_id)
    return {"user": user}

@router.post("")
def parse(user: UserData):
    response = save_user(user)
    return {"response": response}
