import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.pipeline import run_pipeline
from backend.graph import graph  

app = FastAPI()


class DataInput(BaseModel):
    values: list
    query: str = None


@app.post("/forecast")
def forecast(data: DataInput):

    if data.query:
        state = {
            "data": data.values,
            "query": data.query
        }

        result = graph.invoke(state)
        return result

    result = run_pipeline(data.values, data.query)
    return result


@app.post("/forecast/csv")
async def forecast_csv(
    file: UploadFile = File(...),
    target_column: str = Form(None),
    user_query: str = Form(None)
):

    if not target_column:
        raise HTTPException(
            status_code=400,
            detail="You must specify a 'target_column' to tell the model which column of the CSV to forecast."
        )

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Failed to read the file. Please ensure it is a valid CSV."
        )

    if target_column not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{target_column}' not found. Available columns: {list(df.columns)}"
        )

    if not pd.api.types.is_numeric_dtype(df[target_column]):
        raise HTTPException(
            status_code=400,
            detail=f"Column '{target_column}' must contain numeric values."
        )

    values = df[target_column].dropna().tolist()

    if len(values) == 0:
        raise HTTPException(
            status_code=400,
            detail="The selected column has no valid numerical data."
        )

    if user_query:
        state = {
            "data": values,
            "query": user_query
        }

        result = graph.invoke(state)
        return result

    result = run_pipeline(values, user_query)
    return result