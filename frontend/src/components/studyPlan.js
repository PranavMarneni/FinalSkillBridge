import React, { useState, useEffect } from 'react';
import Card from './card'; 
import './studyPlan.css'; 

export default function StudyPlan() {
    const [studyPlan, setStudyPlan] = useState([]);
    const [error, setError] = useState('');

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
                    if (data.study_plan) {
                        setStudyPlan(data.study_plan);
                    } else {
                        setError('No study plan returned from the backend.');
                    }
                } else {
                    setError('Failed to fetch the study plan.');
                }
            } catch (error) {
                setError('An error occurred while fetching the study plan.');
            }
        };

        fetchStudyPlan();
    }, []);

    const renderedPlan = studyPlan.map((item, index) => (
        <Card 
            key={index}
            topic={item.topic}
            text={item.description}
            videos={item.videoLinks}
        />
    ));

    return (
        <div className="study-plan-container">
            <h1>Study Plan</h1>
            <p>Once you submit your job links, a personalized study plan will appear here:</p>
            {error && <p className="error-message">{error}</p>}
            {renderedPlan.length > 0 ? (
                <div className="study-plan-grid">
                    {renderedPlan}
                </div>
            ) : (
                <p>No study plan available yet. Submit job links to get started.</p>
            )}
        </div>
    );
}