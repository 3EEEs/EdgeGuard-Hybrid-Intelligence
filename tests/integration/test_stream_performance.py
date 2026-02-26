import pytest
import numpy as np
import time
import psutil
import os
from src.motion_detection import process_frame

def test_stream_performance_and_memory():
    """
    INTEGRATION TEST: VideoStream -> MotionDetector
    Goal: Process 100 frames to ensure no memory leaks and 
    maintain a frame rate > 30 FPS.
    """
    # 1. SETUP: Create fake "High Def" frames (640x480)
    frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
    frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
    # Add a white box to simulate actual motion
    frame2[100:200, 100:200] = 255 
    
    # Track starting memory usage
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss / (1024 * 1024) # Convert to MB
    
    start_time = time.time()
    frame_count = 100

    # 2. EXECUTION: Pump frames through your logic
    for _ in range(frame_count):
        # We pass the frames into your actual production function
        is_motion, count = process_frame(frame1, frame2)

    end_time = time.time()
    end_mem = process.memory_info().rss / (1024 * 1024)
    
    # 3. ANALYSIS
    duration = end_time - start_time
    fps = frame_count / duration
    mem_growth = end_mem - start_mem

    print(f"\n--- Integration Performance Report ---")
    print(f"FPS: {fps:.2f}")
    print(f"Memory Leak: {mem_growth:.2f} MB")

    # 4. ASSERTIONS
    # Ensure it's fast enough for real-time video (30 FPS)
    assert fps > 30, f"Performance too slow! Only hit {fps:.2f} FPS"
    
    # Ensure memory doesn't grow by more than 5MB during the run
    assert mem_growth < 5.0, f"Potential memory leak! RAM grew by {mem_growth:.2f} MB"