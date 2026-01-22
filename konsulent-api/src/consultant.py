from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field
import json 
from pathlib import Path


class Consultant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    navn: str
    ferdigheter: List[str]
    belastnings_prosent: int

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return f"Consultant(navn={self.navn}, ferdigheter={self.ferdigheter}, belastning_prosent={self.belastnings_prosent})"

# Usage:

if __name__ == "__main__":
    consultant = Consultant(
        navn="Ola Nordmann",
        ferdigheter=["Python", "Django", "FastAPI"],
        belastnings_prosent=75
    )

    # Example multiple consultants:

    consultants = [
        Consultant(
            navn="Kari Nordmann",
            ferdigheter=["JavaScript", "React", "Node.js"],
            belastnings_prosent=50
        ),
        Consultant(
            navn="Per Hansen",
            ferdigheter=["Java", "Spring Boot", "Hibernate"],
            belastnings_prosent=90
        ),
        Consultant(
            navn="Lise Olsen", 
            ferdigheter=["C#", ".NET", "Azure"],
            belastnings_prosent=60
        )
    ]

    # Save to JSON file
    print("Saving consultants to consultants.json")
    data_path = Path(__file__).resolve().parent / "consultants.json"
    data_path.write_text(
        json.dumps([c.model_dump() for c in consultants], indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Saved to: {data_path}")

    