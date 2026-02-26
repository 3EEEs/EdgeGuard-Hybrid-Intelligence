import pytest
import requests

def test_system_dashboard_image_accessibility():
    # 1. Simulate fetching the latest event metadata from the DB
    # In a real system test, this would query your live DynamoDB table
    test_s3_url = "https://edgeguard-testing.s3.amazonaws.com/test_capture.jpg"
    
    # 2. Execution: Try to access the image link the Dashboard would use
    response = requests.get(test_s3_url)
    
    # 3. Validation: Ensure the S3 bucket permissions allow the UI to see the image
    # Note: This checks for 200 (Public) or 403 (if Signed URLs are failing)
    assert response.status_code == 200, "Dashboard will fail to render: S3 image is not accessible."