from fastapi import FastAPI
from controllers import metrics, users, files
import os
from dotenv import load_dotenv


app = FastAPI()

app.include_router(metrics.router)
app.include_router(users.router)
app.include_router(files.router)

@app.get("/my-first-api")
def hello():
  return {"Hello world!"}
