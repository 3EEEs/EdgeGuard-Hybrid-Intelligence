import cv2
import time
import numpy as np
import os

# motion_detection code add-on
from cloud_uploader import CloudUploader
uploader = CloudUploader()

# 0 means default camera, 1 or 2 means external camera
cap = cv2.VideoCapture(0)

# --- Background Subtractor (MOG2) ---
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=True)

# carries the previous frame to check for motion
prev_gray = None

# --- Motion Settings ---
MOTION_THRESHOLD = 2000        # Playing with this number
SUSTAIN_TIME = 3               # Seconds before full clip recording
MIN_MOTION_TIME = 1            # Ignore motion less than 1 sec
CLIP_DURATION = 3              # Seconds
CENTER_THRESHOLD = 50          # Pixels from center to stop early

motion_start_time = None
recording = False
clip_frames = []

# Cooldown timer settings
UPLOAD_COOLDOWN = 0.015  # seconds between uploads (ex 0.1 sec = max 10 uploads/sec)
last_upload_time = 0  # timestamp of last upload


def analyze_clips():
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
            
            # checks the frame_difference and sees if there are 0(black) 25 - 255 (white) pixels of movement
            # this changes pixels seen as moving will get set to 255 which is white for easier to see the difference
            # any movement above 25 color scale of movement gets set to 255 from dark gray to white
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

            motion_pixels = np.sum(thresh > 0)
            if motion_pixels > 2000:
                print("Motion detected!")
                cv2.imshow("camera", frame) # essentially what is sent out, this is the images that the aws will see
            
                # this knows that motion has been detected and 
                # we know frame will be a clear image of the motion at hand so we can send that to aws rekognition


            # cv2.imshow("Live Feed", gray)
            cv2.imshow("Delta", frame_delta)

            # --- Cloud_Uploader Code ---
            current_time = time.time() #sees elapsed time to help maintain upload cooldown
            if current_time - last_upload_time >= UPLOAD_COOLDOWN: # Check if cooldown period has passed

                # Save the image locally first
                filename = f"capture_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                # Upload to AWS via your choice
                url = uploader.upload_frame(filename)
                # Delete local file to fill up local hardware 
                if url:
                    print(f"File live at: {url}")
                    os.remove(filename)
                last_upload_time = current_time  # Only now reset the cooldown

            # moves the current frame to the previous frame holder
            prev_gray = gray
            


            # currently ends the code when q is pressed
            if cv2.waitKey(1) & 0xff == ord('q'):
                break


    cap.release()
    cv2.destroyAllWindows()
