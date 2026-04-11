from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import run_pipeline

app = FastAPI()


class DataInput(BaseModel):
    values: list
    query: str = None

@app.post("/forecast")
def forecast(data: DataInput):
    result = run_pipeline(data.values , data.query)
    return result