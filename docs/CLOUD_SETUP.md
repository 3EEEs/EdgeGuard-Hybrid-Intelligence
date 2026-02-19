# Cloud Infrastructure Setup
**Lead:** Ethan Short

## Infrastructure Overview
The cloud backend uses a serverless event-driven architecture hosted in `us-west-2`.

### Resources Deployed
1. **IAM User (`EdgeGuard_Device`):** - Created with programmatic access keys for the edge device.
   - Policy: `AmazonS3FullAccess`.
   
2. **S3 Bucket (`edgeguard-images-ethan-2026`):**
   - Private bucket for ingestion of images from the edge.
   - Configured with Event Notifications to trigger Lambda on `Put` events.

3. **DynamoDB Table (`EdgeGuard_Events`):**
   - Partition Key: `EventID` (String)
   - Sort Key: `Timestamp` (String)
   - Billing: On-Demand

4. **Lambda Function (`EdgeGuard_Processor`):**
   - Runtime: Python 3.12
   - Permissions: `AmazonRekognitionFullAccess`, `AmazonDynamoDBFullAccess`, `AmazonS3ReadOnlyAccess`.
   - Logic: Extracts S3 key, calls Rekognition `detect_labels`, and writes metadata to DynamoDB.

## How to Test
1. Log into AWS Console.
2. Navigate to S3 -> `edgeguard-images-ethan-2026`.
3. Click **Upload** and select a `.jpg` image from your computer.
4. Navigate to DynamoDB -> `EdgeGuard_Events`.
5. Click **Explore items** to verify the new record appears with AI labels.
