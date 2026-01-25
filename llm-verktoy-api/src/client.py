import os
import httpx
from fastapi import HTTPException


BASE_URL = os.getenv("KONSULENT_API_BASE_URL", "http://konsulent-api:8001")


def tilgjengelighet(konsulent):
    belastning = int(konsulent["belastning_prosent"])
    # Sikrer at tilgjengelighet aldri blir negativ
    return max(0, min(100, 100 - belastning))


async def hent_konsulenter():
    """Hent konsulenter fra den konsulent-api"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BASE_URL}/konsulenter")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")


def filtrer_konsulenter(konsulenter_data, min_tilgjengelighet_prosent, påkrevd_ferdighet):
    """Filtrer konsulenter basert på tilgjengelighet og ferdighet."""
    ferdighet = påkrevd_ferdighet.strip().lower()
    
    filtrert = [
        konsulent for konsulent in konsulenter_data
        if tilgjengelighet(konsulent) >= min_tilgjengelighet_prosent
        and any(ferd.lower() == ferdighet for ferd in konsulent["ferdigheter"])
    ]
    
    return filtrert


def lag_sammendrag(filtrert, min_tilgjengelighet_prosent, påkrevd_ferdighet):
    """Lag sammendrag-respons basert på filtrerte konsulenter."""
    if not filtrert:
        return f"Fant 0 konsulenter med minst {min_tilgjengelighet_prosent}% tilgjengelighet og ferdigheten '{påkrevd_ferdighet}'."
    
    antall = len(filtrert)
    konsulent_form = "konsulent" if antall == 1 else "konsulenter"
    detaljer = " ".join(
        f"{konsulent['navn']} har {tilgjengelighet(konsulent)}% tilgjengelighet."
        for konsulent in filtrert
    )
    
    return f"Fant {antall} {konsulent_form} med minst {min_tilgjengelighet_prosent}% tilgjengelighet og ferdigheten '{påkrevd_ferdighet}'. {detaljer}"


async def hent_konsulenter_sammendrag(min_tilgjengelighet_prosent, påkrevd_ferdighet):
    """Hent og filtrer konsulenter, returnér sammendrag."""
    konsulenter_data = await hent_konsulenter()
    filtrert = filtrer_konsulenter(konsulenter_data, min_tilgjengelighet_prosent, påkrevd_ferdighet)
    return lag_sammendrag(filtrert, min_tilgjengelighet_prosent, påkrevd_ferdighet)
