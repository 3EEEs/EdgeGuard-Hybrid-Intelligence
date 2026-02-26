import os
import pytest
from motion_detection import OUTPUT_DIR

def test_system_storage_readiness():
    """
    SYSTEM TEST: Confirms the environment allows the required directory structure.
    Verifies that the software can create the 'imgs' folder for local buffering.
    """
    # Ensure the directory path defined in motion_detection.py exists or is created
    assert os.path.exists(OUTPUT_DIR), f"Output directory {OUTPUT_DIR} was not created"
    assert os.path.isdir(OUTPUT_DIR), "OUTPUT_DIR path is not a directory"
    
    # Verify write permissions (Optimization Lead needs to know we can save frames)
    test_path = os.path.join(OUTPUT_DIR, "write_test.tmp")
    with open(test_path, "w") as f:
        f.write("test")
    
    assert os.path.exists(test_path), "System lacks write permissions to the image directory"
    os.remove(test_path) # Cleanup
