import React from 'react';
import './Home.css';
import {  Heart, Users, Clock, Languages, Mic} from 'lucide-react';

const HomePage = ({ onStartChat }) => {
  return (
    <div className="home-container">
      {/* 1. HERO SECTION */}
      <header className="hero-section">
        <div className="hero-overlay">
          <div className="hero-content">
            <span className="welcome-tag">Welcome to 2Care.ai</span>
            <h1>Modern Healthcare <br /><span className="text-blue">Powered by AI.</span></h1>
            <p> voice assistant in English, Hindi, or Tamil.</p>
            <div className="hero-btns">
              <button className="btn-primary" onClick={onStartChat}>Start Voice Booking</button>
              <button className="btn-secondary">Find a Doctor</button>
            </div>
          </div>
        </div>
      </header>

      {/* 2. STATS BAR */}
      <section className="stats-bar">
        <div className="stat-card">
          <Users color="#007bff" /> <span>10k+ Patients Served</span>
        </div>
        <div className="stat-card">
          <Heart color="#e91e63" /> <span>50+ Top Specialists</span>
        </div>
        <div className="stat-card">
          <Clock color="#4caf50" /> <span>Zero Wait Booking</span>
        </div>
      </section>

      {/* 3. OUR SERVICES SECTION */}
      <section className="services-section">
        <h2 className="section-title">Our Medical Services</h2>
        <div className="services-grid">
          <ServiceCard 
            title="Cardiology" 
            img="https://images.unsplash.com/photo-1628348068343-c6a848d2b6dd?auto=format&fit=crop&q=80&w=400" 
            desc="Expert heart care and diagnostics with leading cardiologists."
          />
          <ServiceCard 
            title="Dermatology" 
            img="https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&q=80&w=400" 
            desc="Advanced skin treatments and professional clinical dermatology."
          />
          <ServiceCard 
            title="Neurology" 
            img="https://images.unsplash.com/photo-1559757175-5700dde675bc?auto=format&fit=crop&q=80&w=400" 
            desc="Comprehensive brain and nervous system care with latest tech."
          />
          <ServiceCard 
            title="Pediatrics" 
            img="https://storage.googleapis.com/treatspace-prod-media/pracimg/u-564/233.jpeg" 
            desc="Caring medical attention for your children's growth and health."
          />
        </div>
      </section>

      {/* 4. WHY CHOOSE AI SECTION */}
     <section className="advantage-section">
  <div className="advantage-header">
    <span className="blue-pill">Cutting-edge Technology</span>
    <h2>The 2Care.ai Advantage</h2>
    <p>We've combined the world's fastest voice models with smart clinical logic to redefine how you interact with your doctor.</p>
  </div>

  <div className="advantage-grid">
    {/* Image on the left side */}
    <div className="advantage-image-container">
      <img 
        src="https://th.bing.com/th/id/OIP.sD5IU8HNqyQwv5qYrBoAVwHaEc?w=294&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3" 
        alt="Clinical AI Technology" 
        className="main-ai-img"
      />
      
    </div>

    {/* Detailed Feature Cards on the right side */}
    <div className="features-list">
      <div className="adv-card">
        <div className="adv-icon-bg"><Languages size={22} /></div>
        <div className="adv-text">
          <h3>Multilingual Fluency</h3>
          <p>Instantly detects and responds in English, Hindi, or Tamil using Nova-2 deep learning.</p>
        </div>
      </div>

      <div className="adv-card">
        <div className="adv-icon-bg"><Mic size={22} /></div>
        <div className="adv-text">
          <h3>Neural Voice Processing</h3>
          <p>Advanced noise cancellation filters out hospital background noise for clear booking.</p>
        </div>
      </div>

     
    </div>
  </div>
</section>
    </div>
  );
};

const ServiceCard = ({ title, img, desc }) => (
  <div className="service-card">
    <img src={img} alt={title} className="service-img" />
    <div className="service-info">
      <h3>{title}</h3>
      <p>{desc}</p>
      <a href="#" className="read-more">Learn more →</a>
    </div>
  </div>
);

export default HomePage;