from fastapi import APIRouter, UploadFile
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client("s3")

router = APIRouter(
    prefix="/file",
    tags=["files", "general"],
    responses={404: {"description": "Not found"}}
)


@router.post("/save")
async def save(file: UploadFile):
    data = await file.read()
    s3 = boto3.resource("s3")
    obj = s3.Object("chats-json", "test.json")
    obj.put(Body=data)
    return
