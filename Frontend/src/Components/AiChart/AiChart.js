import React, { useEffect, useRef } from 'react';
import { User, Bot, Activity } from 'lucide-react';
import './AiChart.css';

const AiChart = ({ messages, latency }) => {
  const scrollRef = useRef(null);
  useEffect(() => { scrollRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  return (
    <div className="aichart-body">
      <div className="metrics">
        <Activity size={12} />
        {latency ? (
          <span>Proc: {latency.LLM_Generation_Done} | Voice: {latency.TTS_First_Byte_Generated}</span>
        ) : <span>System Ready</span>}
      </div>
      <div className="messages-list">
        {messages.map((msg, i) => (
          <div key={i} className={`msg-row ${msg.role}`}>
            <div className="msg-bubble">
              <small className="msg-label">
                {msg.role === 'user' ? <User size={10}/> : <Bot size={10}/>} {msg.role}
              </small>
              <div>{msg.content}</div>
            </div>
          </div>
        ))}
        <div ref={scrollRef} />
      </div>
    </div>
  );
};
export default AiChart;