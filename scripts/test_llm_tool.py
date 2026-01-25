import requests
import os

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")  # Stored using $env:OPENROUTER_API_KEY

if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

user_prompt = "Finn en konsulent med god tilgjengelighet for et Python-prosjekt"

# (Manuell eller heuristisk mapping – helt ok!)
params = {
    "min_tilgjengelighet_prosent": 20,
    "påkrevd_ferdighet": "python"
}

tool_response = requests.get(
    "http://localhost:8002/tilgjengelige-konsulenter/sammendrag",
    params=params,
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