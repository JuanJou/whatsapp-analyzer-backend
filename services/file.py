from fastapi import UploadFile
import uuid
import io
from db.models import File, FileData
from .vectorization import vectorize
from .analyzer import parse_file, parse_pickle
import boto3
import pickle
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
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

    uuid_for_file = str(uuid.uuid4())
    dataframe_with_lines = await parse_file(content)

    pickle_buffer = io.BytesIO()
    pickle.dump(dataframe_with_lines, pickle_buffer)
    pickle_buffer.seek(0)

    file = save_file_on_bucket(uuid_for_file, pickle_buffer)

    vectorize(uuid_for_file)
    return file


def save_file_on_bucket(file_id, content):
    BUCKET_NAME = "conversations"
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    ENDPOINT = "http://s3:9000"

    try:
        print("Starting upload...")
        s3_client = boto3.resource('s3',
                       endpoint_url=ENDPOINT,
                       aws_access_key_id=AWS_ACCESS_KEY,
                       aws_secret_access_key=AWS_SECRET_KEY,
                       aws_session_token=None,
                       config=boto3.session.Config(signature_version='s3v4'),
                       verify=False
                    )

        return s3_client.Bucket(BUCKET_NAME).put_object(Key=f"{file_id}.pkl", Body=content)
    except NoCredentialsError:
        print("No credentials error")
    except PartialCredentialsError:
        print("Missing credentials error")
    except Exception as e:
        print(f"Unkown error: {e}")

async def read_file(file_id: uuid.UUID):


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
