import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EventCard from './EventCard';

const EventFeed = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetching data from the Cloud (DynamoDB)
  const fetchEvents = async () => {
    try {
      // Fetch from your API Gateway endpoint that triggers a Lambda 
      // to scan your DynamoDB 'EventID' and 'Timestamp' fields
      const response = await axios.get('YOUR_AWS_API_GATEWAY_URL');
      setEvents(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching EdgeGuard events:", error);
    }
  };

  useEffect(() => {
    fetchEvents();
    // Non-Functional Requirement: 10-second latency check
    const interval = setInterval(fetchEvents, 10000); 
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container mt-4">
      <h2>Recent Detections</h2>
      {loading ? (
        <p>Loading motion events...</p>
      ) : (
        <div className="row">
          {events.map(event => (
            <div className="col-md-4 mb-3" key={event.EventID}>
              <EventCard event={event} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EventFeed;