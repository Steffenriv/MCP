# Intern AI-assistent – MCP Demo

Dette repositoriet inneholder en liten demoløsning for en intern AI-assistent basert på konseptet **Model Context Protocol (MCP)**.  
Løsningen består av to Python/FastAPI-mikrotjenester som kjører i separate Docker-containere.

## Tjenester
Vi har to tilgjengelige tjenester, konsulent- og llm vertøy api. Konsulent-apiet fungerer som en server for clienten llm-verktøy-apiet, 
hvor llm-verktøy-apiet behandler dataen videre før den returnerer objektet med et menneskelig sammendrag.

### 1. konsulent-api
Gir tilgang til konsulentdata.

- **Endepunkt:** `GET /konsulenter`
- **Respons:** Forhåndsdefinert liste over konsulenter i JSON-format
- **Felt:** `id`, `navn`, `ferdigheter`, `belastning_prosent`

### 2. llm-verktoy-api
Fungerer som et verktøy-API for en AI-assistent.

- **Endepunkt:** `GET /tilgjengelige-konsulenter/sammendrag`
- **Spørreparametere:**
  - `min_tilgjengelighet_prosent`
  - `påkrevd_ferdighet`
- **Logikk:**
  - Henter data fra `konsulent-api`
  - Filtrerer konsulenter basert på tilgjengelighet og påkrevd ferdighet
  - Returnerer et menneskeleselig sammendrag som JSON


## Teknologi
- Python 3.12
- FastAPI
- Pydantic v2
- Docker & Docker Compose

## Kjøring av prosjektet

### Forutsetninger
- Docker Desktop (Windows/Mac) eller Docker Engine (Linux)
- Docker Compose

### Starte prosjektet

Fra repository root:

```bash
docker compose up --build
```

Dette starter begge tjenestene:
- **konsulent-api** på `http://localhost:8001`
- **llm-verktoy-api** på `http://localhost:8002`

### Teste prosjektet

**1. Hent alle konsulenter:**
```bash
curl http://localhost:8001/konsulenter
```

**2. Hent sammendrag med filter:**
```bash
curl "http://localhost:8002/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=50&påkrevd_ferdighet=python"
```

**3. Swagger dokumentasjon:**
- konsulent-api: `http://localhost:8001/docs`
- llm-verktoy-api: `http://localhost:8002/docs`

### Stoppe prosjektet

```bash
docker compose down
```

### Lokal utvikling (uten Docker)

1. Installer Python 3.12+
2. Installer dependencies for hver tjeneste:

```bash
# konsulent-api
cd konsulent-api
pip install -r requirements.txt

# llm-verktoy-api
cd ../llm-verktoy-api
pip install -r requirements.txt
```

3. Kjør hver tjeneste i separate terminaler:

```bash
# Terminal 1 - konsulent-api
cd konsulent-api/src
python -m uvicorn main:app --port 8001 --reload

# Terminal 2 - llm-verktoy-api
cd llm-verktoy-api/src
KONSULENT_API_BASE_URL=http://localhost:8001 python -m uvicorn main:app --port 8002 --reload
```

## Eksempelforespørsler
```bash
curl http://localhost:8001/konsulenter
```