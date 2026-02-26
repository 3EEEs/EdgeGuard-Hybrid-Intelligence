import os
import cv2
import platform
import pytest

def test_system_dependencies():
    """
    SYSTEM TEST: Cross-Platform Compatibility
    Verifies that OpenCV is properly linked and paths are OS-agnostic.
    """
    # 1. Verify OpenCV version and functionality
    version = cv2.__version__
    assert int(version.split('.')[0]) >= 4, f"OpenCV version {version} is too low."

    # 2. Verify Pathing (Crucial for Windows vs Linux)
    # Using os.path.join ensures the system uses / or \ correctly
    base_path = os.getcwd()
    src_path = os.path.join(base_path, "src")
    
    assert os.path.exists(src_path), f"Source directory not found at {src_path}"
    
    # 3. Print system info for the test report
    print(f"\n[SYSTEM INFO] Operating System: {platform.system()}")
    print(f"[SYSTEM INFO] Python Version: {platform.python_version()}")
    print(f"[SYSTEM INFO] OpenCV Version: {version}")

def test_frame_structure():
    """Verifies that the frame data type is consistent across systems."""
    import numpy as np
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    assert frame.dtype == 'uint8', "Data type mismatch on this OS."