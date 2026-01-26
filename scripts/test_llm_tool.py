import requests
import os
import json

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")  # Stored using $env:OPENROUTER_API_KEY

if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

user_prompt = "Finn en konsulent med god tilgjengelighet for et Python-prosjekt"

# Manuell kall til tool-endepunktet for å hente konsulentdata
params_manuell = {
    "min_tilgjengelighet_prosent": 20,
    "påkrevd_ferdighet": "python"
}

# Automatisk parameterutvinning via LLM for tool-kall
param_prompt = """
Returner KUN gyldig JSON med følgende felter:
- min_tilgjengelighet_prosent (int mellom 0 og 100)
- påkrevd_ferdighet (string)

Ikke skriv noe annet enn JSON.
"""

param_response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": param_prompt},
        {"role": "user", "content": user_prompt},
    ],
)

params_auto = json.loads(param_response.choices[0].message.content)

tool_response = requests.get(
    "http://localhost:8002/tilgjengelige-konsulenter/sammendrag",
    params=params_auto,
).json()

final_prompt = f"""
Bruk følgende tool-respons til å svare brukeren:{tool_response}, ikke finn på informasjon som ikke er i tool-responsen.
"""

resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "user", "content": user_prompt},
        {"role": "system", "content": final_prompt},
    ],
)

print(resp.choices[0].message.content)