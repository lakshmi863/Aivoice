import React from 'react';
import { Mic, MicOff, Send } from 'lucide-react';
import './Footer.css';

const Footer = ({ inputText, setInputText, sendText, isRecording, startRecording, stopRecording }) => (
  <footer className="chat-footer">
    <input 
      className="input-field" 
      placeholder="Type a message..." 
      value={inputText}
      onChange={(e) => setInputText(e.target.value)}
      onKeyDown={(e) => e.key === 'Enter' && sendText()}
    />
    <button className={`icon-btn mic ${isRecording ? 'recording' : ''}`} 
      onMouseDown={startRecording} onMouseUp={stopRecording}>
      {isRecording ? <MicOff size={20}/> : <Mic size={20}/>}
    </button>
    <button className="icon-btn send" onClick={sendText}><Send size={20}/></button>
  </footer>
);
export default Footer;