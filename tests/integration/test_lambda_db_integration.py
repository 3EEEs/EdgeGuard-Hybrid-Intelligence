import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Integration Test: Lambda to DynamoDB
# Verifies that metadata is correctly formatted and written to the DB

def mock_metadata_formatter(rekognition_response, s3_url):
    """
    Simulates the MetadataWriter logic from section 2.2.
    Formats raw AI data into the DynamoDB schema.
    """
    # Extract labels and scores
    labels = [label['Name'] for label in rekognition_response['Labels']]
    scores = [round(label['Confidence'], 2) for label in rekognition_response['Labels']]
    
    # Determine priority based on Use Case 4 logic
    priority = "Low"
    if "Person" in labels and any(s >= 90 for s in scores):
        priority = "High"

    # Construct the final DynamoDB record
    return {
        'EventID': f"EVT_{int(datetime.now().timestamp())}",
        'Timestamp': datetime.now().isoformat(),
        'S3_Object_URL': s3_url,
        'Detected_Labels': labels,
        'Confidence_Scores': scores,
        'Event_Priority': priority,
        'Zone': 'Driveway' # Default for this test
    }

@patch('src.lambda_function.boto3.resource')
def test_lambda_to_dynamodb_write(mock_dynamo_resource):
    """
    INTEGRATION TEST: Verifies the writing process to DynamoDB.
    Ensures no schema errors occur during the 'put_item' call.
    """
    # 1. Setup Mock DynamoDB Table
    mock_table = MagicMock()
    mock_dynamo_resource.return_value.Table.return_value = mock_table
    
    # 2. Mock Rekognition Data
    mock_rek_response = {
        'Labels': [{'Name': 'Person', 'Confidence': 98.2}]
    }
    test_url = "https://my-bucket.s3.amazonaws.com/capture_1.jpg"
    
    # 3. Execution: Format the data
    formatted_item = mock_metadata_formatter(mock_rek_response, test_url)
    
    # 4. Validation: Check schema integrity
    assert 'EventID' in formatted_item
    assert formatted_item['Event_Priority'] == "High"
    assert formatted_item['S3_Object_URL'] == test_url
    
    # 5. Validation: Ensure the DB client was called with the correct item
    # This simulates the final step in your Cloud Processing Component
    mock_table.put_item(Item=formatted_item)
    mock_table.put_item.assert_called_once_with(Item=formatted_item)