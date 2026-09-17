import uuid
from pathlib import Path

import torch
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer, set_seed


MODEL_NAME = "facebook/mms-tts-kan"

print("Loading Kannada MMS TTS model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = VitsModel.from_pretrained(MODEL_NAME)

print("Kannada MMS TTS model loaded successfully!")


# backend/app/generated/audio
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "generated" / "audio"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_speech(
    text: str,
    voice: str,
    speed: float
):
    # Voice is kept for compatibility with the existing API.
    # MMS Kannada currently uses this single Kannada checkpoint.
    if voice not in ["kannada", "kn"]:
        raise ValueError("Only Kannada voice is currently available.")

    # Keep speed within a reasonable range
    speed = max(0.5, min(speed, 2.0))

    # Set speaking rate
    model.speaking_rate = speed

    # Convert text to tokens
    inputs = tokenizer(
        text=text,
        return_tensors="pt"
    )

    # Reproducible generation
    set_seed(555)

    # Generate speech
    with torch.no_grad():
        output = model(**inputs).waveform

    waveform = output[0].cpu().numpy()

    # Create unique filename
    filename = f"{uuid.uuid4()}.wav"
    output_path = AUDIO_DIR / filename

    # Save WAV
    scipy.io.wavfile.write(
        str(output_path),
        rate=model.config.sampling_rate,
        data=waveform
    )

    print(f"Generated audio: {output_path}")

    return filename