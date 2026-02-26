from unittest.mock import patch

import lambda_function
import pytest


@patch("lambda_function.rekognition")
@patch("lambda_function.table")
def test_url_decoding_validation(mock_table, mock_rekognition):
    mock_rekognition.detect_labels.return_value = {"Labels": []}

    # Use Case: Filename has a space encoded as '+'
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "test-bucket"},
                    "object": {"key": "camera+1/my+image.jpg"},
                }
            }
        ]
    }

    lambda_function.lambda_handler(event, None)

    # Verify unquote_plus worked: 'camera+1/my+image.jpg' became 'camera 1/my image.jpg'
    mock_rekognition.detect_labels.assert_called_once_with(
        Image={"S3Object": {"Bucket": "test-bucket", "Name": "camera 1/my image.jpg"}},
        MaxLabels=10,
        MinConfidence=70,
    )
