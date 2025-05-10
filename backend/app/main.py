from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware
allowed_origins = [
    "http://localhost:3001",         # ✅ Vite local dev
    "http://172.19.108.220:3001",    # ✅ LAN IP if accessing from other devices
    "https://yourfrontenddomain.com" # Optional production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to CleanCloud backend! The server is up and running."}
