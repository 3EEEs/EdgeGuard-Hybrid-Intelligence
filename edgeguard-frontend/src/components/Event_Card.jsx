import React from "react";

const Event_Card = ({ event }) => {
  // Helper to translate 's3://' into a standard browser-friendly 'https://' link
  const getImageUrl = (s3Url) => {
    if (!s3Url || !s3Url.startsWith("s3://")) return s3Url;

    // Chops off the 's3://' and splits the bucket name from the file name
    const parts = s3Url.replace("s3://", "").split("/");
    const bucket = parts.shift();
    const key = parts.join("/");

    // Builds the standard AWS public web URL
    return `https://${bucket}.s3.amazonaws.com/${key}`;
  };

  const isHighPriority = event.Detected_Labels?.some(
    (label) => label.Name === "Person" && label.Confidence > 90,
  );

  return (
    <div
      className={`card h-100 ${isHighPriority ? "border-danger shadow" : ""}`}
      style={{ backgroundColor: "#0d1117", border: "1px solid #30363d" }}
    >
      {/* 💥 Here is where the magic translation happens! 💥 */}
      <img
        src={getImageUrl(event.S3_URL)}
        alt="Motion Capture"
        className="card-img-top"
        style={{
          height: "200px",
          objectFit: "cover",
          borderTopLeftRadius: "6px",
          borderTopRightRadius: "6px",
        }}
      />

      <div className="card-body" style={{ padding: "15px" }}>
        <h6 className="card-subtitle mb-2" style={{ color: "#8b949e" }}>
          {new Date(event.Timestamp).toLocaleString()}
        </h6>

        {isHighPriority && (
          <div
            className="badge mb-2"
            style={{
              backgroundColor: "#da3633",
              color: "white",
              padding: "5px 8px",
              borderRadius: "4px",
            }}
          >
            CRITICAL EVIDENCE
          </div>
        )}

        <div className="mt-2">
          <strong style={{ color: "#c9d1d9" }}>AI Labels:</strong>
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "5px",
              marginTop: "8px",
            }}
          >
            {event.Detected_Labels?.map((label, index) => (
              <span
                key={index}
                style={{
                  backgroundColor: "#21262d",
                  border: "1px solid #30363d",
                  color: "#c9d1d9",
                  padding: "3px 8px",
                  borderRadius: "12px",
                  fontSize: "0.8rem",
                }}
              >
                {label.Name}: {Math.round(label.Confidence)}%
              </span>
            ))}
          </div>
        </div>

        <div
          className="mt-3 small"
          style={{ color: "#8b949e", fontSize: "0.8rem" }}
        >
          <span>ID: {event.EventID?.substring(0, 8)}</span>
        </div>
      </div>
    </div>
  );
};

export default Event_Card;
