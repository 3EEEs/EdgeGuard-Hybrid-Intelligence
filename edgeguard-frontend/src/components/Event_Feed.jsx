import React, { useState, useEffect } from "react";
import axios from "axios";
import Event_Card from "./Event_Card.jsx";

const Event_Feed = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const panelStyle = {
    backgroundColor: "#1a1d23",
    border: "1px solid #2d333b",
    borderRadius: "8px",
    padding: "20px",
    height: "90%",
    display: "flex",
    flexDirection: "column",
    color: "#f0f6fc",
    overflowY: "auto",
  };

  const fetchEvents = async () => {
    try {
      const response = await axios.get('https://{api-id}.execute-api.us-west-2.amazonaws.com/prod/events');

      if (Array.isArray(response.data)) {
        const sortedData = response.data.sort(
          (a, b) => new Date(b.Timestamp) - new Date(a.Timestamp),
        );
        setEvents(sortedData);
        setError(null);
      } else {
        console.error("AWS returned non-array data:", response.data);
        setEvents([]);
        setError("AWS URL reached, but the route returned an invalid format.");
      }
    } catch (error) {
      console.error("Error fetching motion events:", error);
      setEvents([]);
      setError("Unable to connect to the AWS API Gateway.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={panelStyle}>
      <div
        style={{
          borderBottom: "1px solid #2d333b",
          marginBottom: "20px",
          paddingBottom: "10px",
        }}
      >
        <h3 style={{ margin: 0, fontSize: "1.2rem" }}>Recent Detections</h3>
      </div>

      <div className="feed-content">
        {loading ? (
          <p style={{ color: "#8b949e" }}>Loading motion events...</p>
        ) : error ? (
          <p style={{ color: "#f85149" }}>{error}</p>
        ) : !Array.isArray(events) || events.length === 0 ? (
          <p style={{ color: "#8b949e" }}>No recent motion detected.</p>
        ) : (
          <div style={{ display: "grid", gap: "15px" }}>
            {events.map((event) => (
              <Event_Card key={event.EventID || Math.random()} event={event} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Event_Feed;
