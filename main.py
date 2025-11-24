from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api import endpoints
from contextlib import asynccontextmanager

import os
import signal

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        """
        create a new process group, all 
        subprocess will inherit this.
        """
        os.setsid()

        yield

        """
        terminate the entire group 
        (including subprocesses)
        """
        os.killpg(os.getpgrp(), signal.SIGTERM)

    except Exception as e:
        print(f"Error: {str(e)}")

app = FastAPI(title="Voice Cloning API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(endpoints.router, prefix="/api")

from fastapi.staticfiles import StaticFiles
import os

# Ensure directories exist
os.makedirs("data/generated", exist_ok=True)

# Mount static files
app.mount("/generated", StaticFiles(directory="data/generated"), name="generated")

@app.get("/")
def read_root():
    return {"message": "Voice Cloning API is running"}
