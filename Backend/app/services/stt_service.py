import os
import json
from deepgram import DeepgramClient

class STTService:
    def __init__(self):
        # Fetch key from environment
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        
       
     
        self.client = DeepgramClient(api_key=self.api_key)

    async def transcribe_audio(self, audio_bytes: bytes):
        try:
            # Ignore tiny noise packets
            if len(audio_bytes) < 500:
                return None, "en"

            # Transcription Options
            options = {
                "model": "nova-2",
                "smart_format": True,
                "detect_language": True,
                "container": "webm"
            }

            # Buffer for audio data
            payload = {"buffer": audio_bytes}

            # Call Deepgram REST API
            response = self.client.listen.rest.v("1").transcribe_file(payload, options)

            # Safely extract transcript
            if hasattr(response, 'results'):
                transcript = response.results.channels[0].alternatives[0].transcript
                detected_lang = getattr(response.results.channels[0], "detected_language", "en")
            else:
                # Dict fallback
                transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                detected_lang = response['results']['channels'][0].get('detected_language', 'en')

            if transcript:
                print(f"STT SUCCESS: {transcript} [{detected_lang}]")
            
            return transcript, detected_lang

        except Exception as e:
            print(f"STT SYSTEM ERROR: {str(e)}")
            return None, "en"