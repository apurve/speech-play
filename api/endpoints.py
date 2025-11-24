from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import AudioSample
from services import tts_service
import os
import uuid
import subprocess

router = APIRouter()

UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/generated"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_uploaded_audio_as_wav(uploaded_file: UploadFile, output_path: str) -> str:
    """
    Save uploaded audio file directly as WAV format using ffmpeg.
    Converts on-the-fly without saving the original file.
    Returns the path to the saved WAV file.
    """
    try:
        # Read the uploaded file content
        file_content = uploaded_file.file.read()
        
        # Use ffmpeg to convert to WAV format (16-bit PCM, mono, 16kHz is good for speech)
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-i", "pipe:0",     # Read from stdin
                "-ar", "16000",     # Sample rate 16kHz
                "-ac", "1",         # Mono channel
                "-f", "wav",        # Force WAV format
                "-y",               # Overwrite output file
                output_path
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Send the file content to ffmpeg through stdin
        stdout, stderr = process.communicate(input=file_content)
        
        if process.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to convert audio file: {stderr.decode()}"
            )
        
        return output_path
    except Exception as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        raise HTTPException(
            status_code=500,
            detail=f"Audio conversion failed: {str(e)}"
        )

@router.post("/clone-voice")
async def clone_voice(
    text: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save uploaded file directly as WAV format (converted on-the-fly)
    wav_filename = f"{uuid.uuid4()}_speaker.wav"
    wav_path = os.path.join(UPLOAD_DIR, wav_filename)
    
    try:
        save_uploaded_audio_as_wav(file, wav_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio upload failed: {str(e)}")
        
    # Save to DB (store the WAV file path)
    db_audio = AudioSample(filename=file.filename, filepath=wav_path)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    
    # Generate speech using the WAV file
    output_filename = f"gen_{uuid.uuid4()}.wav"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    try:
        tts_service.generate_speech(text, wav_path, output_path)
    except Exception as e:
        # Cleanup if something fails
        if os.path.exists(wav_path):
            os.remove(wav_path)
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return the URL path to the generated file
    # Assuming we mount 'generated' at /generated
    return {
        "generated_audio_url": f"/generated/{output_filename}",
        "original_audio_id": db_audio.id
    }
