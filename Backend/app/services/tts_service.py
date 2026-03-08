import httpx
import os

class TTSService:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        self.url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"

    async def text_to_speech_stream(self, text: str):
        """
        Converts text to audio bytes. 
        In a production app, we would stream these bytes directly to the websocket.
        """
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"text": text}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.content # Returns raw audio bytes
            else:
                return None