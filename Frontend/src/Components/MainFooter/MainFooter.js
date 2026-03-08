import React from 'react';
import './MainFooter.css';
import { Facebook, Twitter, Instagram, Linkedin, Mail, Phone, MapPin } from 'lucide-react';

const MainFooter = () => {
  return (
    <footer className="main-site-footer">
      <div className="footer-container">
        {/* Column 1: Brand */}
        <div className="footer-col brand-col">
          <img src="https://2care.ai/images/2care-transparent.png" alt="2Care.ai" className="footer-logo" />
          <p className="footer-desc">
            Redefining clinical appointments with real-time AI voice technology. Accessible, efficient, and multilingual healthcare at your fingertips.
          </p>
          <div className="social-links">
            <a href="#"><Facebook size={18} /></a>
            <a href="#"><Twitter size={18} /></a>
            <a href="#"><Instagram size={18} /></a>
            <a href="#"><Linkedin size={18} /></a>
          </div>
        </div>

        {/* Column 2: Quick Links */}
        <div className="footer-col">
          <h3>Quick Links</h3>
          <ul>
            <li><a href="#">About Us</a></li>
            <li><a href="#">Our Specialists</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Medical Blogs</a></li>
            <li><a href="#">Career</a></li>
          </ul>
        </div>

        {/* Column 3: Medical Services */}
        <div className="footer-col">
          <h3>Services</h3>
          <ul>
            <li><a href="#">Cardiology</a></li>
            <li><a href="#">Neurology</a></li>
            <li><a href="#">Dermatology</a></li>
            <li><a href="#">Pediatrics</a></li>
            <li><a href="#">General Medicine</a></li>
          </ul>
        </div>

        {/* Column 4: Contact Info */}
        <div className="footer-col contact-col">
          <h3>Contact Us</h3>
          <div className="contact-item">
            <MapPin size={18} className="footer-icon" />
            <span>123 Medical Park, Suite 405<br/>Tech City, IN 560001</span>
          </div>
          <div className="contact-item">
            <Phone size={18} className="footer-icon" />
            <span>+91 800-227-324</span>
          </div>
          <div className="contact-item">
            <Mail size={18} className="footer-icon" />
            <span>support@2care.ai</span>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="bottom-container">
          <p>&copy; {new Date().getFullYear()} 2Care.ai. All rights reserved.</p>
          <div className="bottom-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Cookie Policy</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default MainFooter;