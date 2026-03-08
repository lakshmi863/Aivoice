import os
import json
from deepgram import DeepgramClient

class STTService:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        # Initialize client
        self.client = DeepgramClient(self.api_key)

    async def transcribe_audio(self, audio_bytes: bytes):
        try:
            # Ignore tiny audio packets
            if len(audio_bytes) < 500:
                return None, "en"

            # Use a simple dictionary for options (Fixes the ImportError)
            options = {
                "model": "nova-2",
                "smart_format": True,
                "detect_language": True,
                "container": "webm"
            }

            # Call Deepgram using the v1 Listen interface
            payload = {"buffer": audio_bytes}
            response = self.client.listen.rest.v("1").transcribe_file(payload, options)

            # Extract result
            transcript = response.results.channels[0].alternatives[0].transcript
            detected_lang = getattr(response.results.channels[0], "detected_language", "en")

            if transcript:
                print(f"STT SUCCESS: {transcript} [{detected_lang}]")
            
            return transcript, detected_lang

        except Exception as e:
            print(f"STT SYSTEM ERROR: {str(e)}")
            return None, "en"