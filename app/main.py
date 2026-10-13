import os
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

AIPIPE_URL = "https://aipipe.org/openrouter/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-4.1-nano"

app = FastAPI(title="AI Pipe OpenAI-Compatible Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    token = os.getenv("AIPIPE_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="AIPIPE_TOKEN is not configured")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Request body must be valid JSON")

    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Request body must be a JSON object")

    payload.setdefault("model", os.getenv("AIPIPE_MODEL", DEFAULT_MODEL))
    payload["stream"] = False
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            upstream = await client.post(AIPIPE_URL, headers=headers, json=payload)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Upstream model request timed out")
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {type(exc).__name__}")

    try:
        data = upstream.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="AI Pipe returned a non-JSON response")

    return JSONResponse(content=data, status_code=upstream.status_code)

@app.options("/v1/chat/completions")
async def chat_completions_options():
    return JSONResponse(content={}, status_code=204)
