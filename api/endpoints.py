from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import AudioSample
from services import tts_service
import shutil
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "backend/uploads"
OUTPUT_DIR = "backend/generated"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/clone-voice")
async def clone_voice(
    text: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save uploaded file
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Save to DB
    # We store the relative path or absolute path. Let's store relative for portability if possible, 
    # but for now absolute or relative to project root is fine.
    db_audio = AudioSample(filename=file.filename, filepath=file_path)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    
    # Generate speech
    output_filename = f"gen_{uuid.uuid4()}.wav"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    try:
        tts_service.generate_speech(text, file_path, output_path)
    except Exception as e:
        # Cleanup if possible?
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return the URL path to the generated file
    # Assuming we mount 'generated' at /generated
    return {
        "generated_audio_url": f"/generated/{output_filename}",
        "original_audio_id": db_audio.id
    }
