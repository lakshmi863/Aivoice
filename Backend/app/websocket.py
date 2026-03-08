import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.agent.assistant import run_conversation
from app.utils.latency import LatencyTracker
from app.utils.logger import logger

router = APIRouter()
stt_service = STTService()
tts_service = TTSService()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    tracker = LatencyTracker()
    history = [] 

    try:
        while True:
            # 1. Wait for incoming packet
            message = await websocket.receive()
            
            # --- START TIMER IMMEDIATELY ---
            tracker.start() 
            user_input = ""

            if "text" in message:
                payload = json.loads(message["text"])
                user_input = payload.get("text")
                logger.info(f"TEXT INPUT: {user_input}")

            elif "bytes" in message:
                audio_data = message["bytes"]
                logger.info(f"VOICE INPUT RECEIVED: {len(audio_data)} bytes")
                
                # Convert Voice to Text
                user_input, lang = await stt_service.transcribe_audio(audio_data)
                
                if not user_input:
                    logger.warning("STT failed to transcribe any text.")
                    await websocket.send_json({"text": "I couldn't hear you clearly.", "latency": {}})
                    continue
                
                logger.info(f"STT TRANSCRIPTION: {user_input}")
                tracker.log_event("STT_Completed")

            if not user_input:
                continue

            # 2. Reasoning (LLM)
            agent_text = await run_conversation(user_input, history)
            tracker.log_event("LLM_Generation_Done")

            # 3. Synthesis (TTS)
            audio_response = await tts_service.text_to_speech_stream(agent_text)
            tracker.log_event("TTS_First_Byte_Generated")

            # 4. Save History
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": agent_text})
            if len(history) > 10: history.pop(0)

            # 5. Send Audio and Data back
            # IMPORTANT: Send bytes first for speed
            if audio_response:
                await websocket.send_bytes(audio_response)
            
            # Send Metadata (Text and real Latency stats)
            await websocket.send_json({
                "text": agent_text,
                "latency": tracker.get_summary()
            })

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket Global Error: {e}")