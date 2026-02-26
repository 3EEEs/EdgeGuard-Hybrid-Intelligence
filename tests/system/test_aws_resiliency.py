from unittest.mock import patch

import lambda_function
import pytest


@patch("lambda_function.rekognition")
def test_system_failure_rekognition_down(mock_rekognition):
    # Simulate an AWS system outage
    mock_rekognition.detect_labels.side_effect = Exception("AWS Rekognition is down")

    event = {
        "Records": [
            {"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "test.jpg"}}}
        ]
    }

    # System should catch the error and raise it upwards
    with pytest.raises(Exception) as excinfo:
        lambda_function.lambda_handler(event, None)

    assert "AWS Rekognition is down" in str(excinfo.value)
