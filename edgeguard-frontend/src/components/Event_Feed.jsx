// src/components/Event_Feed.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Event_Feed() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);

    // Fetch real data from your local Flask server
    const fetchEvents = () => {
        axios.get('http://127.0.0.1:5000/get_events')
            .then(res => {
                if (res.data && res.data.events) {
                    setEvents(res.data.events);
                }
                setLoading(false);
            })
            .catch(err => {
                console.error("Error fetching events:", err);
                setLoading(false);
            });
    };

    useEffect(() => {
        // Fetch immediately on load
        fetchEvents();
        
        // Optional: Poll for new events every 10 seconds
        const interval = setInterval(fetchEvents, 10000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="panel" style={styles.panel}>
            <h2>Recent Events</h2>
            {loading ? <p>Loading events...</p> : (
                <ul style={styles.list}>
                    {events.map(event => {
                        // Grab the primary label to display
                        const primaryLabel = event.Detected_Labels && event.Detected_Labels.length > 0 
                            ? event.Detected_Labels[0] 
                            : { Name: "Unknown", Confidence: 0 };
                            
                        // Format the timestamp nicely
                        const timeString = new Date(event.Timestamp).toLocaleTimeString();

                        // Convert S3 URI (s3://bucket/key) to a public HTTPS URL if needed
                        // Note: Your bucket needs to be public, or you need to generate presigned URLs in Flask
                        const imgUrl = event.S3_URL.replace("s3://", "https://s3.us-west-2.amazonaws.com/");

                        return (
                            <li key={event.EventID} style={styles.card}>
                                <img src={imgUrl} alt="Detection" style={styles.thumbnail} />
                                <div>
                                    <strong>{primaryLabel.Name} ({Math.round(primaryLabel.Confidence)}%)</strong>
                                    <p style={{margin: 0, fontSize: '0.85rem', color: '#888'}}>{timeString}</p>
                                </div>
                            </li>
                        );
                    })}
                </ul>
            )}
        </div>
    );
}

const styles = {
    panel: { background: '#1a1d24', padding: '1rem', borderRadius: '8px', border: '1px solid #2a2d34', overflowY: 'auto', height: '100%' },
    list: { listStyleType: 'none', padding: 0, margin: 0 },
    card: { display: 'flex', gap: '1rem', padding: '0.5rem', borderBottom: '1px solid #2a2d34', alignItems: 'center' },
    thumbnail: { width: '50px', height: '50px', borderRadius: '4px', objectFit: 'cover', background: '#0f1116' }
};