import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def generate_speech(
    text: str,
    voice: str = "troy"
) -> bytes:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from the .env file")

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty")

    if len(text) > 200:
        raise ValueError(
            "Text must be 200 characters or fewer for this TTS model"
        )

    client = Groq(api_key=api_key)

    response = client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        voice=voice,
        input=text,
        response_format="wav"
    )

    return response.content
