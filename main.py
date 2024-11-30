from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, song
from models.base import Base
from database import engine

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["Authorization", "Content-Type", "x-auth-token"],  # Added x-auth-token
)

app.include_router(auth.router, prefix="/auth")
app.include_router(song.router, prefix="/song")

Base.metadata.create_all(engine)
