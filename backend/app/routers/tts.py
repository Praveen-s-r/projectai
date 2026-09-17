from fastapi import APIRouter
from pydantic import BaseModel

from app.services.tts_service import generate_speech

router = APIRouter()

class SpeechRequest(BaseModel):
    text: str
    voice: str
    speed: float

@router.post("/generate-speech")
def tts(request: SpeechRequest):

    filename = generate_speech(
        request.text,
        request.voice,
        request.speed
    )

    return {
        "audio_url": f"/audio/{filename}"
    }
