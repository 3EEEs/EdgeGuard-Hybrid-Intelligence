# System Interfaces
**Lead:** Michael Wilde

## 1. Frontend <-> Cloud (Data Retrieval)

The Dashboard polls the AWS backend to display motion events in the `Event_Feed.jsx` component. 
    * Protocol: HTTPS/REST
    * Endpoint: `GET /events` via AWS API Gateway
    * Polling Interval: 10 seconds (Compliance with NFR 1).
    * Payload Format:

    ```
    {
        "EventID": "string (UUID)",
        "Timestamp": "string (ISO-8601)",
        "S3_Object_URL": "string (Presigned URL)",
        "Detected_Labels": [
            { "Name": "string", "Confidence": "number" }
        ],
        "Zone": "string"
    }
    ```

## 2. UI <-> Edge (Configuration Sync)

This interface allows for `Filter_Control.jsx` slider to adjust the local detection threshold.

    * Mechanism: The UI writes to a `device_config` table in DynamoDB.
    * Edge Polling: The local Python script checks this value every 60 seconds to update the MOG2 background subtraction sensitivity.
    * Key Parameter: `motion_sensitivity` (Integer: 0-100).

## 3. Edge <-> Cloud (Data Ingestion)

Managed by the local Python component to move data from device to AWS.

    * Image Upload: `PUT` to S3 Bucket `edgegaurd-captures`. 
    * Metadata Trigger: S3 Upload triggers an AWS Lambda function for Rekognition processing.

## 4. UI Internal Logic (Use Case 4) 
Critical Evidence: If `Detected_Labels` contains "Person" with Confidence > 90, the Event_Card.jsx must apply `isHighPriority` styling. 