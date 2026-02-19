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

## Code For Lambda Function
```python

import json
import boto3
import uuid
import urllib.parse
from datetime import datetime
from decimal import Decimal

# Connect to AWS services
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

# Lowercase 'g' to match your DynamoDB table
table = dynamodb.Table('Edgeguard_Events') 

def lambda_handler(event, context):
    # 1. Get the image info from the upload event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        print(f"Processing image: {key} from bucket: {bucket}")
        
        # 2. Send image to Amazon Rekognition
        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=10,
            MinConfidence=70
        )
        
        # 3. Simplify the data and convert floats to Decimals
        detected_labels = []
        for label in response['Labels']:
            detected_labels.append({
                'Name': label['Name'],
                'Confidence': Decimal(str(label['Confidence']))
            })
            
        print(f"Found labels: {detected_labels}")
        
        # 4. Save to DynamoDB
        event_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        table.put_item(
            Item={
                'EventID': event_id,
                'Timestamp': timestamp,
                'S3_URL': f"s3://{bucket}/{key}",
                'Detected_Labels': detected_labels
            }
        )
        
        return {'statusCode': 200, 'body': json.dumps('Success')}
        
    except Exception as e:
        print(e)
        raise e

```
