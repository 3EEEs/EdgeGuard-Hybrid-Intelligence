import pytest
import numpy as np
import cv2
from motion_detection import analyze_clips

def test_analyze_clips_scoring():
    """
    UNIT TEST: Verifies that the scoring math favors clear, centered frames.
    This ensures we only store high-quality data, optimizing storage use.
    """
    # 1. Create a 'Good' Frame: Sharp and Centered
    good_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Add sharp text to ensure a high Laplacian variance (avoiding blur penalty)
    cv2.putText(good_frame, "Sharp", (300, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    
    good_mask = np.zeros((480, 640), dtype=np.uint8)
    # Draw a rectangle in the dead center to minimize distance score and avoid edge penalty
    cv2.rectangle(good_mask, (300, 220), (340, 260), 255, -1)

    # 2. Create a 'Bad' Frame: Blurry and at the Edge
    # Blank black frame will have 0 Laplacian variance, triggering the blur penalty
    bad_frame = np.zeros((480, 640, 3), dtype=np.uint8) 
    
    bad_mask = np.zeros((480, 640), dtype=np.uint8)
    # Draw a rectangle at (0,0) to trigger the 4000-point edge penalty
    cv2.rectangle(bad_mask, (0, 0), (20, 20), 255, -1)

    # 3. Execution: Pass both to the analyzer
    # Based on motion_detection.py logic, good_frame should have a much lower (better) score
    result = analyze_clips([(good_frame, good_mask), (bad_frame, bad_mask)])
    
    # 4. Validation
    assert result is not None, "Analyzer failed to return a frame"
    assert np.array_equal(result, good_frame), "Analyzer chose the wrong (lower quality) frame"
