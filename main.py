from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import metrics, users, files
from routes import file as f
import os
from dotenv import load_dotenv

load_dotenv()
print("ENVIRONMENT",os.environ)

app = FastAPI()

origins = [
        "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics.router)
app.include_router(users.router)
app.include_router(files.router)
app.include_router(f.router)
