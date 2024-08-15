import requests
from logger import logger


def vectorize(file_id: str):
    vectorization_endpoint = "http://ml:8000/chats"
    print(f"[DEBUG] File id: {file_id}")
    response = requests.post(vectorization_endpoint, json={"file_id": file_id})
    print(f"[DEBUG] Vectorization response: {response}")

