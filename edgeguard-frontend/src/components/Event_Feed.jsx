import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Event_Card from './Event_Card.jsx';

const Event_Feed = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  // The panel style
  const panelStyle = {
    backgroundColor: '#1a1d23',
    border: '1px solid #2d333b',
    borderRadius: '8px',
    padding: '20px',
    height: '90%',
    display: 'flex',
    flexDirection: 'column',
    color: '#f0f6fc',
    overflowY: 'auto'
  };

  const fetchEvents = async () => {
    try {
      // Integration: Fetching from Ethan's API Gateway
      const response = await axios.get('YOUR_AWS_API_GATEWAY_URL');
      setEvents(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching motion events:", error);
    }
  };

  useEffect(() => {
    fetchEvents();
    // Non-functional Requirement: 10-second latency check
    const interval = setInterval(fetchEvents, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={panelStyle}>
      <div style={{ borderBottom: '1px solid #2d333b', marginBottom: '20px', paddingBottom: '10px' }}>
        <h3 style={{ margin: 0, fontSize: '1.2rem' }}>Recent Detections</h3>
      </div>

      <div className="feed-content">
        {loading ? (
          <p style={{ color: '#8b949e' }}>Loading motion events...</p>
        ) : events.length === 0 ? (
          <p style={{ color: '#8b949e' }}>No recent motion detected.</p>
        ) : (
          <div style={{ display: 'grid', gap: '15px' }}>
            {events.map((event) => (
              <Event_Card key={event.EventID} event={event} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Event_Feed;