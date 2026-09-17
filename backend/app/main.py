from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.tts import router as tts_router

app = FastAPI(title="ProjectAI - Text To Speech")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/audio",
    StaticFiles(directory=BASE_DIR / "generated" / "audio"),
    name="audio",
)

app.include_router(tts_router)

@app.get("/")
def home():
    return {"message": "ProjectAI Backend Running"}