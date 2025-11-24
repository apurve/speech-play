import os
try:
    import torch
except ImportError:
    torch = None

from gtts import gTTS

# Try to import TTS to allow the app to run even if installation failed
try:
    from TTS.api import TTS
except ImportError:
    TTS = None
    print("WARNING: Coqui TTS not installed. Voice cloning will not work.")

# Global TTS model to avoid reloading on every request
tts_model = None

def get_tts_model():
    global tts_model
    if tts_model is None and TTS is not None and torch is not None:
        try:
            # Using a multi-speaker model that supports zero-shot cloning
            # 'tts_models/multilingual/multi-dataset/your_tts' is a good default for cloning
            print("Loading Coqui TTS model...")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            # specific model for voice cloning
            tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)
            print(f"Coqui TTS model loaded on {device}.")
        except Exception as e:
            print(f"Failed to load Coqui TTS model: {e}")
            tts_model = None
    elif TTS is not None and torch is None:
         print("WARNING: Coqui TTS installed but torch is missing. Voice cloning disabled.")
    return tts_model

def generate_speech(text: str, speaker_wav: str, output_path: str, language: str = "en"):
    """
    Generate speech from text using Voice Cloning if available, otherwise fallback to gTTS.
    
    Args:
        text (str): Text to speak
        speaker_wav (str): Path to the reference audio file for voice cloning
        output_path (str): Path to save the generated audio
        language (str): Language code (default: "en")
    """
    model = get_tts_model()
    
    if model:
        try:
            print(f"Generating voice clone using reference: {speaker_wav}")
            # Coqui TTS generation
            model.tts_to_file(text=text, speaker_wav=speaker_wav, language=language, file_path=output_path)
            print(f"Coqui TTS generated audio saved to: {output_path}")
            return output_path
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error using Coqui TTS: {repr(e)}. Falling back to gTTS.")
            
    # Fallback to gTTS
    print(f"WARNING: Using fallback gTTS. Voice cloning (speaker_wav={speaker_wav}) failed or is not supported.")
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)
    return output_path
