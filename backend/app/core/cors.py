from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app: FastAPI) -> None:
    """
    Setup CORS middleware for the FastAPI application
    """
    # Specific origins for your frontend
    origins = [
        "http://localhost:3000",  # React frontend
        "http://127.0.0.1:3000",
        "http://localhost:8000",  # Backend
        "http://127.0.0.1:8000",
        "http://localhost:8001",  # Alternative backend port
        "http://127.0.0.1:8001",
        "http://192.168.1.132:3000",  # Network IP for frontend
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Use specific origins to allow credentials
        allow_credentials=True,  # Allow credentials for authenticated requests
        allow_methods=["*"],
        allow_headers=["*"],
    )