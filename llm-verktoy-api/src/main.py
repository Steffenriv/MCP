from fastapi import FastAPI, Query

from .client import hent_konsulenter_sammendrag

app = FastAPI()

@app.get("/tilgjengelige-konsulenter/sammendrag")
async def tilgjengelige_konsulenter_sammendrag(
    min_tilgjengelighet_prosent: int = Query(..., ge=0, le=100),
    påkrevd_ferdighet: str = Query(..., min_length=1),
):
    sammendrag = await hent_konsulenter_sammendrag(min_tilgjengelighet_prosent, påkrevd_ferdighet)
    return {"sammendrag": sammendrag}
