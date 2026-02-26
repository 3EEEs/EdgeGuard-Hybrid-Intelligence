from unittest.mock import patch

import lambda_function
import pytest


@patch("lambda_function.rekognition")
@patch("lambda_function.table")
def test_lambda_handler_unit(mock_table, mock_rekognition):
    # 1. Setup mock Rekognition response
    mock_rekognition.detect_labels.return_value = {
        "Labels": [{"Name": "Person", "Confidence": 98.5}]
    }

    # 2. Fake S3 Event
    event = {
        "Records": [
            {"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "test.jpg"}}}
        ]
    }

    # 3. Call your function
    response = lambda_function.lambda_handler(event, None)

    # 4. Assert it succeeded
    assert response["statusCode"] == 200

    # 5. Verify Rekognition was called with correct arguments
    mock_rekognition.detect_labels.assert_called_once_with(
        Image={"S3Object": {"Bucket": "test-bucket", "Name": "test.jpg"}},
        MaxLabels=10,
        MinConfidence=70,
    )
