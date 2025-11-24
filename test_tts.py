import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import tts_service

def test_voice_cloning():
    print("Testing Voice Cloning Service...")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use absolute paths to avoid path resolution issues with torchaudio
    # Note: Using the converted WAV file because the original was actually a WebM file
    speaker_wav = os.path.join(script_dir, "test-data", "test_speaker_converted.wav")
    text = "This is a test of the voice cloning system. No wayyyyyyyyyyy, it is working now."
    output_file = os.path.join(script_dir, "test-data", "test_output.wav")
    
    try:
        output = tts_service.generate_speech(text, speaker_wav, output_file)
        print(f"Success! Audio generated at: {output}")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_voice_cloning()
