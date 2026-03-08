
2Care.ai: Real-Time Multilingual Voice AI Agent
2Care.ai is a cutting-edge, low-latency Voice AI Clinical Receptionist designed to manage the full lifecycle of medical appointments. Patients can interact naturally using their voice to book, reschedule, or cancel appointments in English, Hindi (हिंदी), and Tamil (தமிழ்).

 Live Demo & Documentation
Deployment: https://aivoice-health.onrender.com
Tech Stack: FastAPI, React, MongoDB Atlas, Groq (Llama 3.1), Deepgram.
Latency Goal: < 450ms (Actual: ~300ms - 400ms).

Backend_URL: https://aivoice-health.onrender.com

Frontend_URL: https://aivoice-health.onrender.com

LIVE vedio: 

Architecture Diagram:

<img width="1024" height="1136" alt="AiVoice" src="https://github.com/user-attachments/assets/aeadb763-ad93-4975-840b-e289ee44c4b9" />


home page:

<img width="3508" height="3894" alt="aivoice-health onrender com_" src="https://github.com/user-attachments/assets/84593815-6f2a-42b7-b096-89c2c4f32ae4" />

AiChart page:
<img width="1900" height="867" alt="image" src="https://github.com/user-attachments/assets/a0ea3e6b-35ce-4f44-bee7-63753014c0eb" />

 Key Features
Real-Time Voice-to-Voice: Full-duplex communication using WebSockets (WSS).

Multilingual Support: Automatic language detection and response in English, Hindi, and Tamil.

Appointment Management:

Booking: Intelligent slot searching via specialized doctors.

Rescheduling: Ability to move existing appointments to new slots.

Cancellation: Hassle-free removal of scheduled sessions.

Cloud Persistence: Powered by MongoDB Atlas ensuring appointment records and patient history remain safe across server restarts.

Persistent Memory: AI remembers if a patient has visited before, providing a personalized "Welcome Back" experience.

Conflict Logic: Backend verification prevents double-bookings or scheduling in the past.

 Technology Stack
Layer   | 	Technology
Frontend	React.js, Tailwind CSS, Lucide-React Icons

Backend	FastAPI (Python 3.11), WebSockets

LLM (Reasoning)	Groq Llama-3.1-8b-instant (Ultra-fast inference)

Speech-to-Text	Deepgram Nova-2 (Highest accuracy for diverse accents)

Text-to-Speech	Deepgram Aura Asteria (Human-like medical tone)

Database	MongoDB Atlas (Cloud-hosted NoSQL)

Deployment	Render.com

 Architecture Overview
 
The system follows a non-blocking asynchronous pipeline to minimize latency:

Voice Input: Captured via browser MediaRecorder API, sent as bytes through WebSocket.

STT: Deepgram converts bytes to text and identifies the ISO language code.

Agent Logic: Groq interprets intent and fetches context from MongoDB.

Tool Orchestration: The agent executes Python functions (Tools) to query or modify the database.

Synthesis: Text response is converted to audio bytes by Deepgram Aura.

Audio Output: Bytes are sent back via WebSocket and played immediately in the browser.

 Latency Breakdown
The system is optimized for "Sub-Second Response."

STT (Speech-to-Text): ~80ms - 120ms

LLM (Groq Inference): ~150ms - 200ms

Database (MongoDB Atlas): ~50ms

TTS (Speech Synthesis): ~90ms

TOTAL: ~370ms - 460ms (Successfully hitting the target criteria).

 Installation & Setup
 
1. Prerequisites
Python 3.11+
Node.js (v18+)
MongoDB Atlas Account

3. Backend Setup
   
code

Bash

cd Backend

pip install -r requirements.txt

Create a .env file in the Backend directory:
code

Env

GROQ_API_KEY=your_groq_key

DEEPGRAM_API_KEY=your_deepgram_key

DATABASE_URL=mongodb+srv://<user>:<pass>@cluster0...

Start server:
code

Bash

uvicorn app.main:app --reload

5. Frontend Setup
6. 
code

Bash

cd Frontend

npm install

Edit src/App.js to point to ws://localhost:8000/ws/chat.
code
Bash
npm start

 Validations & Safety
Past Date Blocking: System rejects appointments scheduled before the current system time.
Identity Enforcement: AI is instructed to always ask for the patient's name before finalizing a write to the database.
Duplicate Prevention: The database logic verifies doctor availability before confirming a new slot.
