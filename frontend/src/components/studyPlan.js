import React, { useState, useEffect } from 'react';
import Card from './card'; // Import the Card component
import './studyPlan.css'; // Import CSS for the study plan

export default function StudyPlan() {
    const [studyPlan, setStudyPlan] = useState([]);  // State to store the study plan
    const [error, setError] = useState('');  // State to store errors

    // Fetch the study plan when the component mounts
    useEffect(() => {
        const fetchStudyPlan = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/process-urls/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setStudyPlan(data.study_plan);  // Assuming 'study_plan' is returned by the backend
                } else {
                    setError('Failed to fetch the study plan.');
                }
            } catch (error) {
                setError('An error occurred while fetching the study plan.');
            }
        };

        // Trigger the fetch function
        fetchStudyPlan();
    }, []);

    // Dynamically render the fetched study plan
    const renderedPlan = studyPlan.map((item, index) => (
        <Card 
            key={index}
            topic={item.topic}  // Assuming 'topic' is part of the study plan
            text={item.description}  // Assuming 'description' is part of the study plan
            videos={item.videoLinks}  // Assuming 'videoLinks' is part of the study plan
        />
    ));

    return (
        <div className="study-plan-container">
            <h1>Study Plan</h1>
            <p>Once you submit your job links, a personalized study plan will appear here:</p>
            {error && <p className="error-message">{error}</p>} {/* Show error if any */}
            {renderedPlan.length > 0 ? renderedPlan : <p>No study plan available yet. Submit job links to get started.</p>}
        </div>
    );
}
