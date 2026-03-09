import os
import time
import threading

import cv2
import numpy as np
from flask import Flask, Response, request, jsonify
from flask_cors import CORS


# Add at top with other settings
LOG_ALL_MOTIONS = True 


# Flask Setup
app = Flask(__name__)
CORS(app)

@app.route("/set_logging_mode", methods=["POST"])
def set_logging_mode():
    global LOG_ALL_MOTIONS
    data = request.get_json()
    LOG_ALL_MOTIONS = bool(data.get("log_all", True))
    print(f"Logging mode updated: {LOG_ALL_MOTIONS}")
    return jsonify({"status": "ok", "log_all": LOG_ALL_MOTIONS})

class BudgetTracker:
    def __init__(self, limit=200.000):
        self.limit = limit
        self.spent = 0.000  # Starting point
        self.cost_per_upload = 0.001 

    def log_upload(self):
        self.spent += self.cost_per_upload
        return self.spent

tracker = BudgetTracker(limit=200.000)

# Create imgs folder inside /code if it doesn't exist
OUTPUT_DIR = os.path.join(os.getcwd(), "imgs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# motion_detection code add-on
from .cloud_uploader import CloudUploader

uploader = CloudUploader()

# 0 means default camera, 1 or 2 means external camera
cap = cv2.VideoCapture(0)

# --- Background Subtractor (MOG2) ---
fgbg = cv2.createBackgroundSubtractorMOG2(
    history=500, varThreshold=25, detectShadows=False
)

# --- Global state variables ---
prev_gray = None
motion_start_time = None
short_motion_saved = False
recording = False
clip_frames = []
last_motion_time = None
record_start_time = 0

# --- Motion Settings ---
MOTION_THRESHOLD = 200  # Playing with this number
SUSTAIN_TIME = 5  # Seconds before full clip recording
MIN_MOTION_TIME = 0.3  # Ignore motion less than 0.3 sec
CLIP_DURATION = 6  # Seconds
CENTER_THRESHOLD = 50  # Pixels from center to stop early
NO_MOTION_RESET_TIME = 0.2  # seconds allowed without motion

# Cooldown timer settings
UPLOAD_COOLDOWN = 0.015  # seconds between uploads
last_upload_time = 0  # timestamp of last upload


# ---- Threshold Endpoints ----
@app.route("/set_threshold", methods=["POST"])
def set_threshold():
    global MOTION_THRESHOLD
    data = request.get_json()
    if data is None or "threshold" not in data:
        return jsonify({"error": "Missing threshold value"}), 400
    threshold = int(data["threshold"])
    threshold = max(50, min(400, threshold))
    MOTION_THRESHOLD = threshold
    return jsonify({"status": "ok", "motion_threshold": MOTION_THRESHOLD})

@app.route("/get_threshold", methods=["GET"])
def get_threshold():
    return jsonify({"motion_threshold": MOTION_THRESHOLD})


def analyze_clips(frames):
    best_score = float("inf")
    best_frame = None

    for frame, fg_mask in frames:
        # Clean up noise
        fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)[1]
        fg_mask = cv2.medianBlur(fg_mask, 5)

        contours, _ = cv2.findContours(
            fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
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
        object_center = (x + w // 2, y + h // 2)

        distance = np.sqrt(
            (object_center[0] - frame_center[0]) ** 2
            + (object_center[1] - frame_center[1]) ** 2
        )

        # ----- EDGE PENALTY -----
        edge_margin = 20
        edge_penalty = 0

        if (
            x < edge_margin
            or y < edge_margin
            or x + w > frame_w - edge_margin
            or y + h > frame_h - edge_margin
        ):
            edge_penalty = 4000

        # ----- BLUR PENALTY -----
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        blur_penalty = 0
        if blur_score < 120:
            blur_penalty = 2500

        # ----- FINAL SCORE -----
        score = distance * 4 - area * 0.00005 + edge_penalty + blur_penalty

        if score < best_score:
            best_score = score
            best_frame = frame

    return best_frame


def process_frame(prev_gray_frame, current_gray_frame):
    """
    This function wraps the math you already wrote so the test can see it.
    """
    frame_delta = cv2.absdiff(prev_gray_frame, current_gray_frame)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    motion_pixels = np.sum(thresh > 0)

    is_motion = motion_pixels > MOTION_THRESHOLD
    return bool(motion_pixels > MOTION_THRESHOLD), int(motion_pixels)


def generate_frames():
    """
    This generator runs your main loop continuously, processing motion,
    and yielding the frames to the web server.
    """
    global prev_gray, motion_start_time, short_motion_saved
    global recording, clip_frames, last_motion_time, record_start_time
    global MOTION_THRESHOLD  # allows Flask endpoint updates to be seen here

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converts the frames to be gray
        gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blurs the frame

        if prev_gray is None:
            prev_gray = gray
            continue

        # grabs the difference between the frames
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
                if LOG_ALL_MOTIONS:
                    tracker.log_upload()
                    # TODO add the aws section
                    
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
        fg_mask = fgbg.apply(frame)

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

                    tracker.log_upload()

                    # TODO uncomment the AWS features
                    # url = uploader.upload_frame(filename)
                    # if url:
                    #     print(f"File live at: {url}")
                    #     os.remove(filename)

                recording = False
                motion_start_time = None

        prev_gray = gray  # moves current frame to previous frame holder

        # ----- Overlay threshold + live motion pixel count -----
        cv2.putText(
            frame,
            f"Threshold: {MOTION_THRESHOLD}  Motion: {int(motion_pixels)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0) if motion_pixels > MOTION_THRESHOLD else (200, 200, 200),
            2
        )

        # ----- FLASK WEB STREAMING -----
        # Encode the frame into a JPEG for the browser
        ret_encode, buffer = cv2.imencode(".jpg", frame)
        if not ret_encode:
            continue
        frame_bytes = buffer.tobytes()

        # Yield the formatted image bytes to the web server
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")


# ---- Flask Endpoints ----
@app.route("/video_feed")
def video_feed():
    # This route returns the multipart stream to your Astro frontend
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/get_budget", methods=["GET"])
def get_budget():
    response = jsonify({
        "spent": round(tracker.spent, 3),
        "limit": tracker.limit,
        "remaining": round(tracker.limit - tracker.spent, 3)
    })
    # This prevents the browser from caching the budget value
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__ == "__main__":
    print("Starting EdgeGuard Backend Server...")
    print("Live stream available at: http://127.0.0.1:5000/video_feed")
    # Setting debug=False is important here so the camera doesn't try to initialize twice
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)


