from fastapi import FastAPI, HTTPException
import json 
from pathlib import Path

app = FastAPI()

DATA_PATH = Path(__file__).resolve().parent / "konsulenter.json" 

@app.get("/")
def root():
    return {"message": "Velkommen til Konsulent Management API"}

@app.get("/konsulenter")
def get_konsulenter():
    try:
        if not DATA_PATH.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Data file not found at: {DATA_PATH}",
            )

        consultants_data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

        if not isinstance(consultants_data, list):
            raise HTTPException(
                status_code=500,
                detail="consultants.json must contain a JSON list",
            )

        return consultants_data

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON in consultants.json: {e}",
        )