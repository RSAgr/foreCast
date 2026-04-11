import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from pipeline import run_pipeline

app = FastAPI()


class DataInput(BaseModel):
    values: list
    query: str = None


@app.post("/forecast")
def forecast(data: DataInput):
    result = run_pipeline(data.values, data.query)
    return result


@app.post("/forecast/csv")
async def forecast_csv(
    file: UploadFile = File(...),
    target_column: str = Form(None),
    user_query: str = Form(None)
):
    # 1. Custom explicit error if column is not passed
    if not target_column:
        raise HTTPException(
            status_code=400, 
            detail="You must specify a 'target_column' to tell the model which column of the CSV to forecast."
        )

    # 2. Attempt to parse the CSV file from memory
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read the file. Please ensure it is a valid CSV.")

    # 3. Validation: Does the column exist?
    if target_column not in df.columns:
        raise HTTPException(
            status_code=400, 
            detail=f"Column '{target_column}' not found. Available columns in your CSV are: {list(df.columns)}"
        )
        
    # 4. Validation: Is the column made of numbers?
    if not pd.api.types.is_numeric_dtype(df[target_column]):
        raise HTTPException(
            status_code=400, 
            detail=f"Column '{target_column}' contains non-numeric data. Forecasting requires numbers."
        )

    # Remove empty rows from that column and convert to a pure list
    values = df[target_column].dropna().tolist()

    if len(values) == 0:
        raise HTTPException(
            status_code=400, 
            detail="The selected column has no valid numerical data."
        )

    # Run the exact same pipeline with our extracted CSV values and the optional LLM query
    result = run_pipeline(values, user_query)
    return result