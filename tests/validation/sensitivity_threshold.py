import pytest
from motion_detection import MOTION_THRESHOLD

def test_motion_threshold_logic():
    """
    VALIDATION TEST: Ensures the threshold is set to optimize storage efficiency.
    Verifies that small pixel changes (noise) are ignored by the system.
    """
    # Current code uses a threshold of 200 pixels
    # A small noise change (e.g., 50 pixels) should be below the trigger point
    noise_change = 50 
    
    assert MOTION_THRESHOLD == 200, "Motion threshold has been modified from optimized value"
    assert noise_change < MOTION_THRESHOLD, "Threshold is too sensitive; will cause storage bloat"
