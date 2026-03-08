import os
import json
from deepgram import DeepgramClient

class STTService:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        # Ensure client is initialized
        self.client = DeepgramClient(api_key=self.api_key)

    async def transcribe_audio(self, audio_bytes: bytes):
        try:
            # 1. Minimum sensitivity: Ignore anything under 100 bytes
            if len(audio_bytes) < 100:
                print(f"STT: Buffer too small ({len(audio_bytes)} bytes)")
                return None, "en"

            print(f"STT: Sending {len(audio_bytes)} bytes to Deepgram...")

            # 2. Options for Nova-2
            options = {
                "model": "nova-2",
                "smart_format": True,
                "detect_language": True,
                "container": "webm"
            }

            # 3. Call Deepgram using the most stable v1 interface
            payload = {"buffer": audio_bytes}
            response = self.client.listen.rest.v("1").transcribe_file(payload, options)

            # 4. ROBUST PARSING (Handle both Dict and Pydantic Object)
            transcript = ""
            detected_lang = "en"

            # Convert response to dictionary if it isn't already
            if not isinstance(response, dict):
                try:
                    
                    res_dict = response.to_dict() if hasattr(response, 'to_dict') else response
                except:
                    res_dict = response
            else:
                res_dict = response

            # Navigate the nested Deepgram structure safely
            try:
                # Structure: results -> channels[0] -> alternatives[0] -> transcript
                if hasattr(res_dict, 'results'): # Object access
                    results = res_dict.results
                    channels = results.channels[0]
                    transcript = channels.alternatives[0].transcript
                    detected_lang = getattr(channels, "detected_language", "en")
                else: # Dict access
                    results = res_dict.get('results', {})
                    channels = results.get('channels', [{}])[0]
                    alternatives = channels.get('alternatives', [{}])[0]
                    transcript = alternatives.get('transcript', "")
                    detected_lang = channels.get('detected_language', "en")
            except Exception as parse_err:
                print(f"STT: Parsing logic failed -> {parse_err}")

            if transcript and transcript.strip():
                print(f"STT SUCCESS: '{transcript}' [{detected_lang}]")
                return transcript.strip(), detected_lang
            else:
                print("STT: No words detected in audio stream.")
                return None, "en"

        except Exception as e:
            print(f"STT CRITICAL ERROR: {str(e)}")
            return None, "en"