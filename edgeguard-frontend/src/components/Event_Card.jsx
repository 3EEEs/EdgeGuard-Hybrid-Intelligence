import React from 'react';

const EventCard = ({ event }) => {
  // Use Case 4: Escalating priority for person detection > 90% confidence
  const isHighPriority = event.Detected_Labels.some(
    (label) => label.Name === 'Person' && label.Confidence > 90
  );

  return (
    <div className={`card h-100 ${isHighPriority ? 'border-danger shadow' : ''}`}>
      {/* Retrieve filtered image via S3 URL */}
      <img 
        src={event.S3_Object_URL} 
        alt="Motion Capture" 
        className="card-img-top" 
        style={{ height: '200px', objectFit: 'cover' }}
      />
      
      <div className="card-body">
        <h6 className="card-subtitle mb-2 text-muted">
          {new Date(event.Timestamp).toLocaleString()}
        </h6>
        
        {isHighPriority && (
          <div className="badge bg-danger mb-2">CRITICAL EVIDENCE</div>
        )}

        <div className="mt-2">
          <strong>AI Labels:</strong>
          <div className="d-flex flex-wrap gap-1 mt-1">
            {event.Detected_Labels.map((label, index) => (
              <span key={index} className="badge bg-secondary">
                {label.Name}: {Math.round(label.Confidence)}%
              </span>
            ))}
          </div>
        </div>

        <div className="mt-3 small text-muted">
          <span>Zone: {event.Zone}</span> | <span>ID: {event.EventID.substring(0, 8)}</span>
        </div>
      </div>
    </div>
  );
};

export default EventCard;