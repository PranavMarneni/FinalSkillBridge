import React from 'react';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import Header from './components/header.js'
import Hero from './components/hero.js'
import Form from './components/input.js'
import Plan from './components/studyPlan.js'
import { videos } from './components/videos';
import Video from './components/videoSlider'
import PdfExtractor from './components/upload.js'

function App() {
  return (
    <div>
      <Header /> {/* Render the Header component */}
      <Hero />
      <PdfExtractor/>
      <Form />
      <Plan />
      <Video videos = {videos}/>
      {/*Don't like how all this isn't in its own component*/}
      {/* Rest of your app content */}
    </div>
  );
}

export default App;