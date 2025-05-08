#!/bin/bash

# One-shot script to set up CleanCloud Backend using FastAPI

set -e

echo "🚀 Creating backend project directory..."
mkdir -p ~/cleancloud/backend
cd ~/cleancloud/backend

echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install fastapi uvicorn sqlalchemy pydantic bcrypt passlib python-jose python-dotenv

echo "📝 Creating project folder structure..."
mkdir -p app/models app/routes app/schemas app/core app/db

touch app/__init__.py
touch app/models/__init__.py
touch app/routes/__init__.py
touch app/schemas/__init__.py
touch app/core/__init__.py
touch app/db/__init__.py

echo "🔧 Creating starter files..."

# main.py
cat > main.py <<EOF
from fastapi import FastAPI
from app.routes import auth, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")

@app.get("/")
def read_root():
    return {"message": "CleanCloud API is running"}
EOF

# .env
cat > .env <<EOF
SECRET_KEY="your_secret_key_here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL="sqlite:///./cleancloud.db"
EOF

echo "✅ CleanCloud backend setup completed!"
echo "👉 Next steps:"
echo "  1. Implement models, schemas, routes inside 'app/'"
echo "  2. Run the server: source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
