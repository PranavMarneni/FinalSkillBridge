import React from 'react';
import './card.css';  // Import CSS for the card component

const Card = ({ topic, text, videos }) => {
    return (
        <div className="card">
            <h2>{topic}</h2>
            <p>{text}</p>
            {videos && videos.length > 0 && (
                <div>
                    <h3>Related Videos:</h3>
                    <ul>
                        {videos.map((video, index) => (
                            <li key={index}>
                                <a href={video} target="_blank" rel="noopener noreferrer">
                                    Watch Video {index + 1}
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default Card;
