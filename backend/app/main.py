from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CleanCloud API",
    description="Backend for managing AWS idle resources securely.",
    version="1.0.0"
)

# CORS middleware
allowed_origins = [
    "http://localhost:3001",         # For local development (Vite/React)
    "http://172.19.108.220:3001",    # Local network access (LAN IP)
    "https://yourfrontenddomain.com" # Replace with your real production frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/", tags=["Root"])
def root():
    """
    Health check endpoint to confirm the backend is running.
    """
    logger.info("Root endpoint accessed.")
    return {"message": "✅ CleanCloud backend is up and running!"}
