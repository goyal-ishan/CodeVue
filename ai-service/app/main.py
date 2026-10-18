from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.interview import router as interview_router

app = FastAPI(
    title="CodeVue AI Interviewer",
    description="AI-powered technical interview service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(interview_router)


@app.get("/")
def home():
    return {
        "message": "CodeVue AI Interviewer API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
