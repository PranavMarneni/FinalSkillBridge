import React from 'react';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import Header from './components/header.js'
import Hero from './components/hero.js'
import Form from './components/input.js'
import Plan from './components/studyPlan.js'
import { videos } from './components/videos';
import Video from './components/videoSlider'

function App() {
  return (
    <div>
      <Header /> {/* Render the Header component */}
      <Hero />
      <Form />
      <Plan />
      <Video videos = {videos}/>
      {/*Don't like how all this isn't in its own component*/}
      <div>Reccomended Practice</div>
      <div>
        <h1>Project Ideas</h1>
        <p>Project ideas generated here</p>
      </div>
      {/* Rest of your app content */}
    </div>
  );
}

export default App;