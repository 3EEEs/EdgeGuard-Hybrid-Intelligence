# EdgeGuard Hybrid Intelligence: User Manual

This manual provides instructions to install, configure, and operate the EdgeGuard Hybrid Intelligence system.

---

## High-Level Description

**EdgeGuard Hybrid Intelligence** is an automated security and monitoring solution designed to bridge the gap between local edge computing and cloud-based analytics. 

When motion is detected, the system:
* **Captures** the frame where the motion occurred.
* **Uploads** the frame to an AWS S3 bucket.
* **Prepares** the data for advanced cloud processing via Amazon Rekognition.

This hybrid approach ensures that users only consume cloud bandwidth and storage when meaningful events occur, providing a cost-effective and responsive security layer.

## How to Install the Software

In order to use the EdgeGuard software, you must configure both your local environment and your AWS infrastructure.

### Prerequisites
  * **Python**: Version 3.8 or higher is recommended
  * **Hardware**: A functional webcam or integrated camera.
  * **AWS Account**: Access to an S3 Bucket and IAM credentials (Access Key ID and Secret Access Key).

### Step-by-Step Installation
  1) **Navigate to the project directory**:
  ```bash
  cd ~/EdgeGuard-Hybrid-Intelligence/code
  ```
  2) **Initialize Virtual Environment**:
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```
  3) **Install Libraries**:
  ```bash
  pip install boto3 python-dotenv opencv-python numpy
  ```
  4) **Configure Credentials**:
     * Create a .env file in the project root to store your AWS details
       * ```AWS_ACCESS_KEY_ID```
       * ```AWS_SECRET_ACCESS_KEY```
       * ```AWS_REGION``` (e.g., ```us-west-2```)
       * ```S3_BUCKET_NAME```

## How to Run the Software
1) Activate the Environment: Ensure your virtual environment is active (source env/bin/activate
2) Lanch the Motion Detection Engine:
   * Run the following command:
   ```bash
   python3 motion_detection.py
   ```
3) System Operation:
   * **Delta Window:** Displays the live mathematical difference between frames.
   * **Camera Window:** Automatically displays the captured event when motion is detected.
   * **Console Output:** Displays the S3 URL of the uploaded image (e.g., File live at: ```https://...```).
4) Exit: Press the 'q' key while the camera window is focused to stop the program.

## Work in Progress:
As noted in the functional sections, the following features are currently under development
  * **Background subtraction:** Not yet implemented in the main loop.
  * **User UI:** Sensitivity sliders and zone-based filtering has not been implemented yet.
  * **Dashboard:** Automated notifications and event filtering controls has not been implemented yet.
  * **Automation:** A script to automatically compile all code and pre-reqs has not been implemented yet.

## How to Use the Software

**EdgeGuard Hybrid Intelligence** captures motion from your camera feed, uploads relevant frames to the cloud, and analyzes them using AWS services. Here's how to interact with the system:

### Motion Detection (Edge)

- The Python script continuously monitors your camera for motion using frame differencing and Gaussian blur.
- When motion exceeds the sensitivity threshold:
  - A frame is captured and temporarily saved locally.
  - The frame is uploaded to your AWS S3 bucket using the `CloudUploader` component.
  - Local copies are automatically deleted after successful upload.
- Users can preview motion detection in the application window.
- **Work in Progress:** User-adjustable sensitivity sliders and zone-based filtering are not fully implemented. Backgorund subtraction is not yet fully implemented.

### Cloud Upload and Processing

- Uploaded frames trigger AWS Lambda functions for further analysis.
- Amazon Rekognition detects objects in the images and returns labels with confidence scores.
- Metadata (timestamp, detected labels, confidence scores, priority, S3 URL) is stored in DynamoDB.
- **Work in Progress:** Full integration with the dashboard and automated notifications are pending.

### Web Dashboard (Upcoming)

- The dashboard will display captured frames with labels, timestamps, and metadata.
- Users will be able to filter events and review high-priority alerts.
- **Work in Progress:** Event filtering controls, analytics, and alert notifications are still under development.

### Notes
- Ensure all prerequisites are installed
- Python virtual environment activated
- The system currently requires manual execution of the edge script to start capturing motion.
- Some advanced features like real-time alerts and detailed dashboard filtering are not yet available.

--- 

## How to Report a Bug

Thank you for helping improve **EdgeGuard Hybrid Intelligence**! To report a bug, please provide as much detail as possible so our team can reproduce and fix the issue quickly.

### Steps to Report a Bug

1. **Check Existing Issues**  
   Before reporting, see if the bug has already been reported in the [Issues section](https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence/issues).

2. **Create a New Issue**  
   Click **New Issue** in GitHub. Copy the template below into the issue body.

3. **Fill Out the Template**  
   Provide detailed information in each section. Include screenshots, logs, or error messages when possible.

4. **Submit the Issue**  
   Our team will review it and respond as quickly as possible.

---

### Bug Report Template

**Title:**  
*(Short descriptive title of the problem)*

**Description:**  
*(Describe the problem clearly. What is happening? What did you expect to happen instead?)*

**Steps to Reproduce:**  
*(Provide the exact steps to reproduce the issue)*  
1.  
2.  
3.  

**Expected Behavior:**  
*(What should have happened if the program worked correctly)*

**Actual Behavior:**  
*(What actually happened. Include error messages or unexpected output)*

**Screenshots or Logs:**  
*(Attach any screenshots, console logs, or error messages if applicable)*

**System Information:**  
- Operating System:  
- Program Version:  
- Browser / Runtime (if applicable):  

**Reproducibility:**  
*(Does this issue occur every time, sometimes, or rarely?)*

**Additional Context:**  
*(Any other information that may help diagnose the issue, such as configuration settings or related issues)*

---

## Known Bugs
1. [motion_detection.py Fails to Upload Frame Due to NoneType Bucket in S3 Client] (https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence/issues/1)















