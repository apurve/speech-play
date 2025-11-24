from gtts import gTTS
import os

def generate_speech(text: str, speaker_wav: str, output_path: str, language: str = "en"):
    print(f"WARNING: Using fallback gTTS. Voice cloning (speaker_wav={speaker_wav}) is NOT supported in this mode.")
    
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)
    return output_path
