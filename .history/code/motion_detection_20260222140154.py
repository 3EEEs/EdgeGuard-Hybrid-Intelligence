import cv2
import time
import numpy as np
import os

# for test saving

# Create imgs folder inside /code if it doesn't exist
OUTPUT_DIR = os.path.join(os.getcwd(), "imgs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# motion_detection code add-on
from cloud_uploader import CloudUploader
uploader = CloudUploader()

# 0 means default camera, 1 or 2 means external camera
cap = cv2.VideoCapture(0)

# --- Background Subtractor (MOG2) ---
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=False)

# carries the previous frame to check for motion
prev_gray = None

# --- Motion Settings ---
MOTION_THRESHOLD = 200         # Playing with this number
SUSTAIN_TIME = 5               # Seconds before full clip recording
MIN_MOTION_TIME = 0.3          # Ignore motion less than 0.3 sec
CLIP_DURATION = 6              # Seconds
CENTER_THRESHOLD = 50          # Pixels from center to stop early
last_motion_time = None
NO_MOTION_RESET_TIME = 0.2     # seconds allowed without motion

motion_start_time = None
short_motion_saved = False
recording = False
clip_frames = []



# Cooldown timer settings
UPLOAD_COOLDOWN = 0.015  # seconds between uploads (ex 0.1 sec = max 10 uploads/sec)
last_upload_time = 0  # timestamp of last upload


def analyze_clips(frames):

    best_score = float('inf')
    best_frame = None
    prev = None

    for frame in frames:

        fg_mask = fgbg.apply(frame)

        # Clean up noise
        fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)[1]
        fg_mask = cv2.medianBlur(fg_mask, 5)
        
        
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            continue

        # Use largest contour (likely you)
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area < 4000:
            continue

        x, y, w, h = cv2.boundingRect(largest)

        frame_h, frame_w = frame.shape[:2]
        frame_center = (frame_w // 2, frame_h // 2)
        object_center = (x + w//2, y + h//2)

        distance = np.sqrt(
            (object_center[0] - frame_center[0])**2 +
            (object_center[1] - frame_center[1])**2
        )

        # ----- EDGE PENALTY -----
        edge_margin = 20
        edge_penalty = 00

        if x < edge_margin or y < edge_margin or \
            x+w > frame_w - edge_margin or \
            y+h > frame_h - edge_margin:
            edge_penalty = 1000

        # ----- BLUR PENALTY -----
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        blur_penalty = 0
        if blur_score < 100:
            blur_penalty = 300

        # ----- FINAL SCORE -----
        score = (
            distance * 3.5
            - area * 0.00005
            + edge_penalty
            + blur_penalty
        )

        if score < best_score:
            best_score = score
            best_frame = frame
            
    return best_frame


# ----  Main LOOP  -----

# this makes the camera run continuously until I press q
while True:
    ret, frame = cap.read()
    if not ret:
        break
            
        # cv2.imshow("Live Feed not gray", frame) # this is non blurred, non 
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converts the frames to be greay
    gray = cv2.GaussianBlur(gray, (21,21), 0)   # blurs the frame

        
    if prev_gray is None:
        prev_gray = gray
        continue

    # grabs the diffrence between the frames
    frame_delta = cv2.absdiff(prev_gray, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        
    motion_pixels = np.sum(thresh > 0)
    current_time = time.time()


    # ----  MOTION DETECTED  ----

    
    if motion_pixels > MOTION_THRESHOLD:
    
        last_motion_time = None
        if motion_start_time is None:
            motion_start_time = current_time
            short_motion_saved = False

        motion_duration = current_time - motion_start_time

        # SHORT MOTION
        if (
            MIN_MOTION_TIME <= motion_duration < SUSTAIN_TIME
            and not short_motion_saved
        ):
            print("Short motion detected")

            filename = f"short_motion_{int(time.time())}.jpg"
            full_path = os.path.join(OUTPUT_DIR, filename)

            print("Saving frame to:", full_path)  # Debug confirmation
            cv2.imwrite(full_path, frame)

            short_motion_saved = True

        # SUSTAINED MOTION
        elif motion_duration >= SUSTAIN_TIME and not recording:
            print("Sustained motion detected — recording clip")
            recording = True
            clip_frames = []
            record_start_time = current_time

    else:
        if last_motion_time is None:
            last_motion_time = current_time

        if current_time - last_motion_time > NO_MOTION_RESET_TIME:
            motion_start_time = None
            short_motion_saved = False
            last_motion_time = None

    # -----   RECORDING    -----
    
    if recording:
        clip_frames.append((frame.copy(), fg_mask.copy()))
        if current_time - record_start_time >= CLIP_DURATION:
            print("Analyzing clip...")
            best_frame = analyze_clips(clip_frames)

            if best_frame is not None:
                filename = f"capture_{int(time.time())}.jpg"
                full_path = os.path.join(OUTPUT_DIR, filename)

                print("Saving frame to:", full_path)  # Debug confirmation
                cv2.imwrite(full_path, best_frame)

                print(f"Best frame saved locally: {filename}")
                
                # Upload to AWS via your choice
                # TODO uncomment the AWS features
                # url = uploader.upload_frame(filename)

                # Delete local file to fill up local hardware 
                # if url:
                #     print(f"File live at: {url}")
                #     os.remove(filename)
                # last_upload_time = current_time  # Only now reset the cooldown

            recording = False
            motion_start_time = None

    
    # ----- update display -----

    cv2.imshow("Live", frame)
    cv2.imshow("Delta", frame_delta)

    prev_gray = gray            # moves the current frame to the previous frame holder
    


    # currently ends the code when q is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
