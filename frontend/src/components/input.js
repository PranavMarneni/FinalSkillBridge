import React, { useState, useEffect } from 'react';
import './input.css';

const InputForm = () => {
    const [jobLink, setJobLink] = useState('');  // State to store the current job link
    const [submittedUrls, setSubmittedUrls] = useState([]);  // State to track submitted URLs
    const [alertMessage, setAlertMessage] = useState('');  // State to show messages

    // Fetch submitted URLs from the backend when the component loads
    useEffect(() => {
        const fetchSubmittedUrls = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/urls/');
                if (response.ok) {
                    const data = await response.json();
                    setSubmittedUrls(data);  // Update state with URLs from the backend
                } else {
                    setAlertMessage('Error fetching submitted URLs.');
                }
            } catch (error) {
                setAlertMessage('Network error: Could not fetch submitted URLs.');
            }
        };

        fetchSubmittedUrls();  // Fetch the URLs on component load
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (jobLink.trim()) {
            // API call for submitting the job link
            try {
                const response = await fetch('http://127.0.0.1:8000/api/submit-url/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: jobLink }),
                });

                if (response.ok) {
                    setAlertMessage(`Link submitted successfully: ${jobLink}`);
                    
                    // Update the submitted URLs list on successful submission
                    setSubmittedUrls((prevUrls) => [...prevUrls, jobLink]);

                    // Clear the input field
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
        // Trigger the backend to process the URLs
        try {
            const response = await fetch('http://127.0.0.1:8000/api/process-urls/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setAlertMessage('Processing URLs... Check the result: ' + JSON.stringify(data));
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
            <p className="input-subtitle">Please place the links in the form underneath:</p>
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
                    <button
                        type="button"
                        className="done-button"
                        onClick={handleDoneSubmitting}
                    >
                        Done Submitting
                    </button>
                </div>
            </form>

            {/* Display the list of submitted URLs */}
            <div className="submitted-urls">
                <h3>Submitted URLs:</h3>
                <ul>
                    {submittedUrls.map((url, index) => (
                        <li key={index}>{url.url}</li>  // Assuming each URL object has a 'url' field
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default InputForm;
