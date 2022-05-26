from fastapi import FastAPI
from controllers import metrics

app = FastAPI()

app.include_router(metrics.router)

@app.get("/my-first-api")
def hello():
  return {"Hello world!"}
