from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    api_key=os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("groq api key is missing from the .env file")

    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.3,
        api_key=api_key
    )
