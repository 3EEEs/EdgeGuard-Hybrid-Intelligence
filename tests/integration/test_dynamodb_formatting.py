from decimal import Decimal
from unittest.mock import patch

import lambda_function
import pytest


@patch("lambda_function.rekognition")
@patch("lambda_function.table")
def test_lambda_to_dynamodb_integration(mock_table, mock_rekognition):
    # Simulate AWS Rekognition returning a label
    mock_rekognition.detect_labels.return_value = {
        "Labels": [{"Name": "Car", "Confidence": 95.123}]
    }

    event = {
        "Records": [
            {"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "test.jpg"}}}
        ]
    }

    lambda_function.lambda_handler(event, None)

    # Verify DynamoDB put_item was called
    mock_table.put_item.assert_called_once()

    # Extract the exact item your code tried to save to DynamoDB
    put_args = mock_table.put_item.call_args[1]["Item"]

    # Assert data was integrated and formatted correctly
    assert put_args["S3_URL"] == "s3://test-bucket/test.jpg"
    assert put_args["Detected_Labels"][0]["Name"] == "Car"
    assert isinstance(put_args["Detected_Labels"][0]["Confidence"], Decimal)
