import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def transcribe_audio(
    audio_bytes: bytes,
    filename: str = "answer.webm",
    language: str | None = None
) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from the .env file")

    if not audio_bytes:
        raise ValueError("Audio file is empty")

    client = Groq(api_key=api_key)

    audio_file = (filename, audio_bytes)

    options = {
        "file": audio_file,
        "model": "whisper-large-v3-turbo",
        "response_format": "json",
        "temperature": 0.0
    }

    if language:
        options["language"] = language

    transcription = client.audio.transcriptions.create(**options)

    return transcription.text.strip()
