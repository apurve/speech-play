# Voice Cloning App - Backend

This is the backend service for the Voice Cloning application, built with **FastAPI**. It handles audio recording uploads, persistence via **SQLite**, and speech generation (currently using **gTTS** as a fallback).

## Prerequisites

- Python 3.9+
- `pip`

## Setup

1.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

Start the development server:

```bash
python -m uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
API Documentation (Swagger UI) is available at `http://localhost:8000/docs`.

## API Endpoints

### `POST /api/clone-voice`

Uploads a recorded voice sample and generates speech from text.

- **Form Data**:
    - `text` (string): The text to convert to speech.
    - `file` (file): The recorded audio file (WAV/MP3).

- **Response**:
    ```json
    {
        "generated_audio_url": "/generated/gen_uuid.wav",
        "original_audio_id": 1
    }
    ```

## Project Structure

- `main.py`: Application entry point.
- `database.py`: Database connection and session management.
- `models.py`: SQLAlchemy models.
- `api/endpoints.py`: API route definitions.
- `services/tts_service.py`: Logic for text-to-speech generation.
- `uploads/`: Directory for storing uploaded user recordings.
- `generated/`: Directory for storing generated speech files.
