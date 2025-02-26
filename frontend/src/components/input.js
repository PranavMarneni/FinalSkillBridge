import React, { useState, useEffect } from 'react';
import './input.css';

const InputForm = () => {
    const [jobLink, setJobLink] = useState('');
    const [submittedUrls, setSubmittedUrls] = useState([]);
    const [alertMessage, setAlertMessage] = useState('');

    useEffect(() => {
        const fetchSubmittedUrls = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/url-list/');
                if (response.ok) {
                    const data = await response.json();
                    setSubmittedUrls(data);
                } else {
                    setAlertMessage('Error fetching submitted URLs.');
                }
            } catch (error) {
                setAlertMessage('Network error: Could not fetch submitted URLs.');
            }
        };

        fetchSubmittedUrls();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (jobLink.trim()) {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/submit-url/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: jobLink }),
                });

                if (response.ok) {
                    const newUrl = await response.json();
                    setSubmittedUrls((prevUrls) => [...prevUrls, newUrl]);
                    setAlertMessage(`Link submitted successfully: ${jobLink}`);
                    setJobLink('');
                } else {
                    setAlertMessage('There was an error submitting the link.');
                }
            } catch (error) {
                setAlertMessage('Network error: Could not submit the link.');
            }
        } else {
            setAlertMessage('Please enter a valid job link.');
        }
    };

    const handleDoneSubmitting = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/process-urls/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setAlertMessage('Processing completed. View the study plan on the Study Plan page.');
            } else {
                setAlertMessage('Error occurred during processing.');
            }
        } catch (error) {
            setAlertMessage('Network error: Could not process the links.');
        }
    };

    return (
        <div className="input-form">
            <h2 className="input-title">Add Your Job Links</h2>
            <p className="input-subtitle">Please place the links in the form below:</p>
            <form onSubmit={handleSubmit}>
                <input
                    type="url"
                    placeholder="Job links go here"
                    value={jobLink}
                    onChange={(e) => setJobLink(e.target.value)}
                    className="job-input"
                    required
                />
                <p className="alert-message">{alertMessage}</p>

                <div className="button-container">
                    <button type="submit" className="submit-button">Keep Submitting More</button>
                </div>
            </form>

            <div className="submitted-urls">
                <h3>Submitted URLs:</h3>
                <ul>
                    {submittedUrls.map((url, index) => (
                        <li key={index}>{url.url}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default InputForm;
