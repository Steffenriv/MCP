from fastapi import FastAPI, HTTPException
from consultant import Consultant
import json 
from pathlib import Path

app = FastAPI()

DATA_PATH = Path(__file__).resolve().parent / "consultants.json"  # src/consultants.json

@app.get("/")
def root():
    return {"message": "Velkommen til Konsulent Management API"}

@app.get("/konsulenter")
def get_consultants():
    try:
        if not DATA_PATH.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Data file not found at: {DATA_PATH}",
            )

        raw = DATA_PATH.read_text(encoding="utf-8")
        consultants_data = json.loads(raw)

        if not isinstance(consultants_data, list):
            raise HTTPException(
                status_code=500,
                detail="consultants.json must contain a JSON list (array) of consultants",
            )

        consultants = [Consultant(**c) for c in consultants_data]

        # Return proper JSON
        return {"consultants": [c.model_dump() for c in consultants]}

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON in consultants.json: {e}",
        )
    except Exception as e:
        # catches Pydantic validation errors etc.
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load consultants: {type(e).__name__}: {e}",
        )

@app.post("/konsulenter")
def add_consultant(navn : str, ferdigheter: list[str], belastnings_prosent: int):
    # Add new consultant object to the JSON file
    consultant = Consultant(
        navn=navn,
        ferdigheter=ferdigheter,
        belastnings_prosent=belastnings_prosent
    )
    
    # Read existing consultants
    if DATA_PATH.exists():
        consultants_data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    else:
        consultants_data = []
    
    # Append new consultant
    consultants_data.append(consultant.model_dump())
    
    # Write back to file
    DATA_PATH.write_text(
        json.dumps(consultants_data, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    return {"message": f"Consultant {consultant.name} added successfully"}
