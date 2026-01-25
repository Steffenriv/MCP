from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field
import json 
from pathlib import Path


class Konsulent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    navn: str
    ferdigheter: List[str]
    belastning_prosent: int

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return f"Konsulent(navn={self.navn}, ferdigheter={self.ferdigheter}, belastning_prosent={self.belastning_prosent})"

# Usage:

if __name__ == "__main__":
    # Example enkel Konsulent:
    konsulent1 = Konsulent(
        navn="Ola Nordmann",
        ferdigheter=["Python", "Django", "FastAPI"],
        belastning_prosent=75
    )

    # Example flere konsulenter:
    Konsulents = [
        Konsulent(
            navn="Kari Nordmann",
            ferdigheter=["JavaScript", "React", "Node.js"],
            belastning_prosent=50
        ),
        Konsulent(
            navn="Per Hansen",
            ferdigheter=["Java", "Spring Boot", "Hibernate"],
            belastning_prosent=90
        ),
        Konsulent(
            navn="Lise Olsen", 
            ferdigheter=["C#", ".NET", "Azure"],
            belastning_prosent=60
        ),
        Konsulent(
            navn="Jens Johansen", 
            ferdigheter=["Go", "Kubernetes", "python"],
            belastning_prosent=30
        ),
        Konsulent(
            navn="Ola Nordmann",
            ferdigheter=["Python", "Django", "FastAPI"],
            belastning_prosent=75
        )
    ]

    # Save to JSON file
    print("Lagrer til konsulenter.json")
    data_path = Path(__file__).resolve().parent / "konsulenter.json"
    if data_path.exists():
        print(f"Overskriver eksisterende fil: {data_path}")
    data_path.write_text(
        json.dumps([c.model_dump() for c in Konsulents], indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Lagret til: {data_path}")

    