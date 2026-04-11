from fastapi import FastAPI
from pydantic import BaseModel
from backend.pipeline import run_pipeline

app = FastAPI()


class DataInput(BaseModel):
    values: list


@app.post("/forecast")
def forecast(data: DataInput):
    result = run_pipeline(data.values)
    return result