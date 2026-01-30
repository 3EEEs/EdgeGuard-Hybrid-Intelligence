import cv2
import time
import numpy as np
import os


# 0 means default camera, 1 or 2 means external camera
cap = cv2.VideoCapture(0)

# carries the previous frame to check for motion
prev_gray = None

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
        
        # checks the frame_difference and sees if there are 0(black) 25 - 255 (white) pixels of movement'
        # this changes pixels seen as moving will get set to 255 which is white for easier to see the difference
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        motion_pixels = np.sum(thresh > 0)
        if motion_pixels > 2000:
            print("Motion detected!")
            cv2.imshow("camera", frame) # essentially what is sent out, this is the images that the aws will see
        
            # this knows that motion has been detected and 
            # we know frame will be a clear image of the motion at hand so we can send that to aws rekognition


        # cv2.imshow("Live Feed", gray)
        cv2.imshow("Delta", frame_delta)

        # moves the current frame to the previous frame holder
        prev_gray = gray
        


        # currently ends the code when q is pressed
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
