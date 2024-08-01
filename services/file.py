from fastapi import UploadFile
import uuid
from db.models import File, FileData
from .analyzer import parse_file, parse_pickle
import boto3
import os


def validate(file: UploadFile):
    print(f"File: {file.content_type}")

    match file.content_type:
        case "text/plain":
            return file
        case _:
            raise TypeError("File has wrong type")


def is_valid_uuid(uuid_to_test):
    try:
        # check for validity of Uuid
        uuid_obj = uuid.UUID(uuid_to_test, version=4)
    except ValueError:
        return "Invalid Uuid"
    return "Valid Uuid"

async def process_file(content):
    uuid_for_file = uuid.uuid4()
    #dataframe_with_lines = await parse_file(lines)
    #dataframe_with_lines.to_pickle(f"{uuid_for_file}")
    return await save_file_on_bucket(uuid_for_file, content)


async def save_file_on_bucket(file_id, content):
    BUCKET_NAME = "whatsapp-convs"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY_ID = os.getenv("AWS_SECRET_KEY_ID")
    ENDPOINT = os.getenv("S3_ENDPOINT")
    print(AWS_SECRET_KEY_ID)
    print(AWS_ACCESS_KEY_ID)

    print("Starting upload...")
    s3_client = boto3.resource('s3',
                   endpoint_url=ENDPOINT,
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_KEY_ID,
                   aws_session_token=None,
                   config=boto3.session.Config(signature_version='s3v4'),
                   verify=False
                )

    return await s3_client.Bucket(BUCKET_NAME).put_object(Key=f"{file_id}.txt", Body=content)

async def read_file(file_id: uuid.UUID):
    BUCKET_NAME = "whatsapp-convs"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY_ID = os.getenv("AWS_SECRET_KEY_ID")
    ENDPOINT = os.getenv("S3_ENDPOINT")


    s3_client = boto3.client('s3',
                   endpoint_url=ENDPOINT,
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_KEY_ID,
                   aws_session_token=None,
                   config=boto3.session.Config(signature_version='s3v4'),
                   verify=False
                )

    pickle_file = s3_client.download_file(Bucket=BUCKET_NAME,Filename=f"{file_id}.pkl", Key=f"{file_id}.pkl")
    return await parse_pickle(file_id)
