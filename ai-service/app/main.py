import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.interview import router as interview_router

app = FastAPI(
    title="CodeVue AI Interviewer",
    description="AI-powered technical interview service",
    version="1.0.0",
)

frontend_env = os.getenv("FRONTEND_URL", "").rstrip("/")

origins = [
    "https://codevue-frontend.onrender.com",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

if frontend_env:
    origins.append(frontend_env)
    if not frontend_env.startswith("http"):
        origins.append(f"https://{frontend_env}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_router)

@app.get("/")
def home():
    return {"message": "CodeVue AI Interviewer API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "codevue-api"}