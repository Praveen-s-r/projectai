import gc
import uuid
from pathlib import Path

import torch
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer, set_seed


MODEL_NAME = "facebook/mms-tts-kan"

# Keep CPU memory usage lower
torch.set_num_threads(1)

print("Loading Kannada MMS TTS model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = VitsModel.from_pretrained(MODEL_NAME)

# The posterior encoder is not required for text-to-speech inference
del model.posterior_encoder
gc.collect()

# BF16 significantly reduces memory usage while working on CPU
model = model.to(dtype=torch.bfloat16)

gc.collect()

print("Kannada MMS TTS model loaded successfully!")
print("Using BF16 low-memory inference.")


# backend/app/generated/audio
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "generated" / "audio"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_speech(
    text: str,
    voice: str,
    speed: float
):
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
    with torch.inference_mode():
        output = model(**inputs).waveform

    # Convert BF16 output to float32 before saving as WAV
    waveform = output[0].float().cpu().numpy()

    # Create unique filename
    filename = f"{uuid.uuid4()}.wav"
    output_path = AUDIO_DIR / filename

    scipy.io.wavfile.write(
        str(output_path),
        rate=model.config.sampling_rate,
        data=waveform
    )

    print(f"Generated audio: {output_path}")

    return filename