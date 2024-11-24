import React from 'react';
import Slider from 'react-slick';
import './videoSlider.css'; // Import CSS for styling

export default function VideoSlider({ videos }) {
    // Slider settings
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3, // Number of videos to show at once
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    infinite: true,
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            }
        ]
    };

    return (
        <div className="video-slider">
            <h2>Recommended Udemy Videos</h2>
            <Slider {...settings}>
                {videos.map((video, index) => (
                    <a key={index} href={video.link} target="_blank" rel="noopener noreferrer">
                        <img 
                            src={video.thumbnail} 
                            alt={video.title} 
                            className="video-thumbnail"
                        />
                    </a>
                ))}
            </Slider>
        </div>
    );
}
