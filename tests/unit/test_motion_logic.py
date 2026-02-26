import pytest
import numpy as np
import cv2
from src.motion_detection import analyze_clips

def test_motion_pixel_threshold_logic():
    thresh_mock = np.zeros((100, 100), dtype=np.uint8)
    cv2.rectangle(thresh_mock, (0, 0), (10, 10), 255, -1)
    motion_pixels = np.sum(thresh_mock > 0)
    
    # 11x11 = 121 pixels. Still under 200 threshold.
    assert motion_pixels == 121 
    assert motion_pixels < 200

def test_analyze_clips_filters_small_objects():
    # 50x50 = 2500 area. Should be ignored by 'if area < 4000'
    frame = np.zeros((500, 500, 3), dtype=np.uint8)
    mask = np.zeros((500, 500), dtype=np.uint8)
    cv2.rectangle(mask, (0, 0), (50, 50), 255, -1) 
    
    clip_frames = [(frame, mask)]
    best_frame = analyze_clips(clip_frames)
    assert best_frame is None

def test_analyze_clips_selects_valid_motion():
    # 100x100 = 10,000 area. Should pass 'area < 4000'
    # We put it in the center to get a good 'Distance' score
    frame = np.zeros((500, 500, 3), dtype=np.uint8)
    mask = np.zeros((500, 500), dtype=np.uint8)
    cv2.rectangle(mask, (200, 200), (300, 300), 255, -1)
    
    # We must add something to the frame so it isn't "blurry" (Laplacian var > 120)
    # Drawing a white grid helps pass the blur penalty
    for i in range(0, 500, 20):
        cv2.line(frame, (i, 0), (i, 500), (255, 255, 255), 1)

    clip_frames = [(frame, mask)]
    best_frame = analyze_clips(clip_frames)
    assert best_frame is not None