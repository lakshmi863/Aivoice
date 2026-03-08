import os
from deepgram import DeepgramClient

class STTService:
    def __init__(self):
        # Fetch key
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        # Initialize client correctly with keyword argument
        self.client = DeepgramClient(api_key=self.api_key)

    async def transcribe_audio(self, audio_bytes: bytes):
        try:
            # 1. Lower threshold (Sensitive Check)
            # 500 was too high; 200 allows short words like 'hi' or 'yes'
            if len(audio_bytes) < 200:
                print(f"STT DEBUG: Audio too short ({len(audio_bytes)} bytes)")
                return None, "en"

            # 2. Setup Transcription Options
            options = {
                "model": "nova-2",
                "smart_format": True,
                "detect_language": True,
                "container": "webm"
            }

            payload = {"buffer": audio_bytes}

            # 3. Call Deepgram REST API
            # Note: We use .listen.rest.v("1") for maximum stability
            response = self.client.listen.rest.v("1").transcribe_file(payload, options)

            # 4. ROBUST EXTRACTION (Fixed for SDK v6)
            # In v6, the response is a Pydantic Model with nested properties
            try:
                # Try accessing via dot notation (SDK standard)
                if hasattr(response, 'results'):
                    result_data = response.results
                    channels = result_data.channels[0]
                    transcript = channels.alternatives[0].transcript
                    # Attempt to get language, default to 'en'
                    detected_lang = getattr(channels, "detected_language", "en")
                else:
                    # Fallback for dictionary responses
                    transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                    detected_lang = response['results']['channels'][0].get('detected_language', 'en')

                # If we got text, return it
                if transcript and transcript.strip() != "":
                    print(f"STT SUCCESS: '{transcript}' [{detected_lang}]")
                    return transcript, detected_lang
                else:
                    print("STT DEBUG: Deepgram connected but no words were heard.")
                    return None, "en"

            except Exception as extraction_err:
                print(f"STT DATA ERROR: Failed to parse result -> {extraction_err}")
                return None, "en"

        except Exception as e:
            print(f"STT SYSTEM CRASH: {str(e)}")
            return None, "en"