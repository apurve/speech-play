import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import UploadFile
from io import BytesIO
from api.endpoints import save_uploaded_audio_as_wav

def test_direct_wav_conversion():
    """Test that we can convert uploaded files directly to WAV format."""
    print("Testing direct WAV conversion...")
    
    # Use the existing test speaker file as input
    test_input = "test-data/test_speaker.wav"  # This is actually a WebM file
    test_output = "test-data/test_direct_conversion.wav"
    
    # Simulate an uploaded file
    with open(test_input, "rb") as f:
        file_content = f.read()
    
    # Create a mock UploadFile
    class MockUploadFile:
        def __init__(self, content):
            self.file = BytesIO(content)
            self.filename = "test.webm"
    
    mock_file = MockUploadFile(file_content)
    
    try:
        # Test the direct conversion
        result = save_uploaded_audio_as_wav(mock_file, test_output)
        print(f"✅ Direct conversion successful: {result}")
        
        # Verify the output file exists and is a real WAV
        if os.path.exists(test_output):
            file_size = os.path.getsize(test_output)
            print(f"✅ Output file created: {test_output} ({file_size} bytes)")
            
            # Check if it's a real WAV file
            os.system(f"file {test_output}")
        else:
            print("❌ Output file was not created")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_wav_conversion()
