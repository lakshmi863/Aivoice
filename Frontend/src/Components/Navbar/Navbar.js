import React from 'react';
import './Navbar.css';

const Navbar = ({ isConnected }) => (
  <nav className="navbar">
    <img src="https://2care.ai/images/2care-transparent.png" alt="2Care Logo" className="logo" />
    <div className={`status-pill ${isConnected ? 'online' : 'offline'}`}>
      <span className="dot"></span>
      {isConnected ? 'Online' : 'Connecting...'}
    </div>
  </nav>
);
export default Navbar;