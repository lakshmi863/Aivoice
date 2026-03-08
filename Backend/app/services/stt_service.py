import os
import json
from deepgram import DeepgramClient, PrerecordedOptions

class STTService:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        # Ensure client is initialized
        self.client = DeepgramClient(self.api_key)

    async def transcribe_audio(self, audio_bytes: bytes):
        try:
            # 1. Ignore tiny audio files (usually noise or accidental clicks)
            if len(audio_bytes) < 500:
                print("STT: Audio too short, ignoring.")
                return None, "en"

            # 2. Setup Payload and Options correctly for v3 SDK
            # Using the Options object is more stable than a dictionary in some SDK sub-versions
            payload = {"buffer": audio_bytes}
            
            options = {
                "model": "nova-2",
                "smart_format": True,
                "detect_language": True,
                "container": "webm"
            }

            # 3. Call Deepgram
            # If '.prerecorded' fails, this will catch the specific error
            response = self.client.listen.prerecorded.v("1").transcribe_file(payload, options)

            # 4. Extract results (V3 SDK uses a data model)
            # Some versions use response.results, others use response['results']
            if hasattr(response, 'results'):
                transcript = response.results.channels[0].alternatives[0].transcript
                detected_lang = getattr(response.results.channels[0], "detected_language", "en")
            else:
                # Fallback for dict-based response
                transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                detected_lang = response['results']['channels'][0].get('detected_language', 'en')

            if transcript:
                print(f"STT SUCCESS: {transcript} [{detected_lang}]")
            else:
                print("STT DEBUG: Deepgram returned 200 OK but NO TEXT was detected.")

            return transcript, detected_lang

        except Exception as e:
            print(f"STT SYSTEM ERROR: {str(e)}")
            return None, "en"