import pytest
from src.cloud_uploader import CloudUploader

def test_uploader_initialization():
    """
    INTEGRATION TEST: Verifies component readiness for cloud storage offloading.
    Ensures that environmental variables for S3 are properly loaded.
    """
    # Initialize the uploader (uses os.getenv for AWS keys)
    uploader = CloudUploader()
    
    # Check if the bucket name was successfully loaded (Required for S3 integration)
    assert uploader.bucket_name is not None, "S3_BUCKET_NAME not found in environment"

