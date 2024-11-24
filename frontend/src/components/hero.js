import React from 'react';
import './hero.css'; // Ensure the CSS file enhances visuals

const Hero = () => {
  return (
    <section className="hero">
      <h1 className="hero-title">Bridge the Gap to Your Dream Job</h1>
      <p className="hero-subtitle">
        Unlock your potential with a tailored learning plan designed just for you. 
      </p>
      <div className="scroll-prompt">
        <span className="arrow">⬇️</span>
        <p>Scroll down to start your journey</p>
      </div>
    </section>
  );
};

export default Hero;
