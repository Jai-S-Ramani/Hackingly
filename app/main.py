from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.routes.health import router as health_router
from app.routes.verify import router as verify_router
from app.routes.registrations import router as registrations_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and default event on startup
    init_db()
    yield

app = FastAPI(
    title="VerifyAI - Hackingly Identity Verification Platform",
    description="AI-Powered Identity & Eligibility Verification for Hackathon Registrations (PS-003)",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontends and dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api/v1
app.include_router(health_router, prefix="/api/v1")
app.include_router(verify_router, prefix="/api/v1")
app.include_router(registrations_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Welcome to VerifyAI - AI-Powered Verification Platform for Hackingly",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
