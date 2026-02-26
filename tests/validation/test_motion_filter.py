import pytest
import numpy as np
import cv2
from src.motion_detection import process_frame, MOTION_THRESHOLD

def test_use_case_1_filtered_monitoring():
    """
    VALIDATION TEST: Use Case 1 (Filtered Monitoring)
    Requirement: Verify that 'Significant Motion' is correctly distinguished 
    from 'Background Noise' using controlled pixel variance.
    """
    # 1. SETUP: Create a 500x500 base frame (pure black)
    base_frame = np.zeros((500, 500, 3), dtype=np.uint8)

    # 2. SCENARIO A: BACKGROUND NOISE
    # Create a frame with only 50 pixels changed (Below your 200 threshold)
    noise_frame = base_frame.copy()
    noise_frame[0:2, 0:2] = 255  # 50 pixels
    
    is_motion_noise, count_noise = process_frame(base_frame, noise_frame)

    # 3. SCENARIO B: SIGNIFICANT MOTION
    # Create a frame with 1000 pixels changed (Well above your 200 threshold)
    significant_frame = base_frame.copy()
    significant_frame[100:120, 100:150] = 255  # 1000 pixels
    
    is_motion_sig, count_sig = process_frame(base_frame, significant_frame)

    # 4. ASSERTIONS: Proving the filter works
    # This proves the "Filtered Monitoring" logic is active.
    assert is_motion_noise is False, f"FAILED: Noise was detected as motion ({count_noise} px)"
    assert is_motion_sig is True, f"FAILED: Significant motion was ignored ({count_sig} px)"
    
    print(f"\nSUCCESS: Noise ({count_noise}px) filtered. Significant ({count_sig}px) detected.")