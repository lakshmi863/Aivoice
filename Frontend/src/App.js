import React, { useState, useEffect, useRef, useCallback } from 'react';
import Navbar from './Components/Navbar/Navbar';
import AiChart from './Components/AiChart/AiChart';
import Footer from './Components/Footer/Footer';
import HomePage from './Components/Home/Home'; // Fixed to match your import
import MainFooter from './Components/MainFooter/MainFooter'; // Fixed to match your import

const WS_URL = "ws://localhost:8000/ws/chat";

function App() {
  // --- UI STATES ---
  const [showChat, setShowChat] = useState(false); 
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [latency, setLatency] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  // --- REFS FOR CORE LOGIC ---
  const ws = useRef(null);
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);

  // --- 1. WEBSOCKET CONNECTION ---
  const connectWS = useCallback(() => {
    ws.current = new WebSocket(WS_URL);

    ws.current.onopen = () => {
      console.log("Connected to 2Care AI Backend");
      setIsConnected(true);
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      console.log("Disconnected. Reconnecting in 3 seconds...");
      setTimeout(connectWS, 3000); 
    };

    ws.current.onmessage = async (event) => {
      if (typeof event.data === "string") {
        const data = JSON.parse(event.data);
        if (data.text) {
          setMessages(prev => [...prev, { role: 'assistant', content: data.text }]);
        }
        if (data.latency) {
          setLatency(data.latency);
        }
      } 
      else {
        const audioBlob = new Blob([event.data], { type: 'audio/mp3' });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
      }
    };
  }, []);

  useEffect(() => {
    connectWS();
    return () => {
      if (ws.current) ws.current.close();
    };
  }, [connectWS]);

  // --- 2. ACTIONS ---
  const sendText = () => {
    if (!inputText.trim() || !isConnected) return;
    ws.current.send(JSON.stringify({ text: inputText }));
    setMessages(prev => [...prev, { role: 'user', content: inputText }]);
    setInputText("");
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      audioChunks.current = [];
      mediaRecorder.current.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunks.current.push(event.data);
      };
      mediaRecorder.current.onstop = () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
          ws.current.send(audioBlob);
          setMessages(prev => [...prev, { role: 'user', content: "🎤 [Voice Message Sent]" }]);
        }
      };
      mediaRecorder.current.start();
      setIsRecording(true);
    } catch (err) { alert("Microphone error."); }
  };

  const stopRecording = () => {
    if (mediaRecorder.current && isRecording) {
      mediaRecorder.current.stop();
      setIsRecording(false);
      mediaRecorder.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  // --- 4. RENDER ---
  return (
    <div style={{ position: 'relative', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* 1. Navbar at the very top */}
      <Navbar isConnected={isConnected} />
      
      {/* 2. Main Page Content (Wraps Home and Footer for scrolling) */}
      <main style={{ flex: 1 }}>
        <HomePage onStartChat={() => setShowChat(true)} />
        
        {/* ADDING THE MAIN FOOTER HERE */}
        <MainFooter />
      </main>

      {/* 3. AI CHAT MODAL (Z-Index ensures it floats above) */}
      {showChat && (
        <div style={overlayStyle}>
          <div style={modalStyle}>
            <div style={closeBar}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <img 
                  src="https://2care.ai/images/2care-transparent.png" 
                  alt="Logo" 
                  style={{ height: '24px', width: 'auto', filter: 'brightness(0) invert(1)' }} 
                />
                <div style={{ display: 'flex', flexDirection: 'column' }}>
                  <span style={{ fontWeight: 'bold', fontSize: '14px', lineHeight: '1' }}>
                    AI Assistant
                  </span>
                  <small style={{ fontSize: '10px', opacity: 0.8, marginTop: '2px' }}>
                    Multilingual Voice Mode
                  </small>
                </div>
              </div>
              <button onClick={() => setShowChat(false)} style={closeBtn}>✖ Close Assistant</button>
            </div>

            <AiChart messages={messages} latency={latency} />
            
            <Footer 
               inputText={inputText} 
               setInputText={setInputText} 
               sendText={sendText} 
               isRecording={isRecording} 
               startRecording={startRecording} 
               stopRecording={stopRecording} 
            />
          </div>
        </div>
      )}
    </div>
  );
}

// --- CSS-IN-JS OBJECTS ---

const overlayStyle = { 
  position: 'fixed', 
  top: 0, left: 0, width: '100%', height: '100%', 
  background: 'rgba(0,0,0,0.8)', 
  display: 'flex', justifyContent: 'center', alignItems: 'center', 
  zIndex: 1000 
};

const modalStyle = { 
  width: '450px', maxWidth: '95vw', height: '85vh', 
  background: 'white', borderRadius: '24px', 
  display: 'flex', flexDirection: 'column', 
  overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.4)' 
};

const closeBar = { 
  padding: '15px 20px', background: '#111', color: 'white', 
  display: 'flex', justifyContent: 'space-between', alignItems: 'center' 
};

const closeBtn = { 
  background: '#dc3545', border: 'none', color: 'white', 
  padding: '6px 12px', borderRadius: '8px', cursor: 'pointer', 
  fontSize: '11px', fontWeight: 'bold' 
};

export default App;