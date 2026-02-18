

## How to Use the Software

EdgeGuard Hybrid Intelligence captures and processes meaningful video events using local motion detection and cloud-based analysis. This guide explains how to interact with the system after it has been started.

### Motion Detection (Edge)

- When motion is detected:
  - The frame is displayed in a preview window.
  - The frame is temporarily saved locally.
  - The frame is uploaded automatically to AWS S3 for cloud processing.
  
- Cooldown and Filtering:
  - A cooldown timer prevents excessive uploads.
  - Only frames meeting the motion threshold are uploaded.
  - This reduces unnecessary cloud processing costs.

### Cloud Processing (AWS)

- Uploaded frames are analyzed by AWS Lambda functions using Amazon Rekognition.
- Detected objects are labeled and stored in DynamoDB with metadata.
- Users can access processed events via the web dashboard (functionality in progress).

### Web Dashboard (Work in Progress)

- The dashboard will display captured frames, AI-detected labels, timestamps, and event metadata.
- Users will eventually be able to filter events by label, zone, or priority.
- Real-time notifications for high-priority events (SMS/email) are planned.

### Notes on Missing Functionality

- Dashboard filtering, notifications, and some analytics are still under development.
- Edge settings like sensitivity sliders and zone selection may be partially implemented.

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

At this time, there are **no known bugs**.  
This section will be updated as the project progresses and any issues are discovered.  
_Work in progress – check back regularly for updates!_





