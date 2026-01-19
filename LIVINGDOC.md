# Project Proposal: EdgeGuard Hybrid Intelligence
## Date: January 19, 2026 Course: CS 362


### Team Info
* Ethan Short – API and Cloud Integration
* Calvin Grabowski – Lead Motion Detection Lead
* Michael Wilde – Video Processing Lead
* Samuel Dressel – Motion Detection and Storage Optimization Lead


## Project Artifacts

Code Repository: [Link](https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence)

Project Board: [Github Project](https://github.com/users/3EEEs/projects/2/views/1)

Google Doc: [Project Deliverable 1](https://docs.google.com/presentation/d/1xFujLNTsQRAWX66ZN-khSHP7Vj1CQskHdH3TL1hhviU/edit)

Report Format: [Link](https://canvas.oregonstate.edu/courses/2026970/assignments/10302739)

## Communication Plan

Channels: Discord and text groupchat for daily synchronous chat; GitHub Issues for task tracking; Weekly meeting after class and as needed.

## Rules:
* All code changes must go through a Pull Request with at least one review.
* "Blockers" must be communicated in Discord immediately.
* Response time expectation: Within 24 hours on weekdays.
* Weekly project reports due between Friday - Sunday of every week. Rotation Ethan, Calvin, Samuel, Michael

## Product Description

* **Abstract:** This project introduces an automated image detection application designed to streamline video monitoring by filtering out irrelevant motion. By integrating motion-triggered capture with Amazon Rekognition, the system identifies specific entities (such as people, animals, or objects) and ignores environmental noise. This solution reduces the time spent reviewing raw footage and provides businesses with actionable, filtered data, ultimately lowering operational costs and improving security efficiency.

* **Goal:** Takes snippets of movement from a video and saves those snippets. This saves total storage, saves money by making our customers not having to submit as much to amazon rekognition, and it makes it easier for humans to go through the snippets. Our product would send only exact frames or small clips to amazon rekognition to save money, by sending less frames than other services and less expensive than other options.

* **Current Practice:** Most video surveillance and monitoring systems rely on continuous recording or full video streaming to the cloud, where all footage is stored and analyzed. This approach results in high storage costs, excessive cloud processing fees, and large volumes of irrelevant footage that users must manually review.

* **Novelty:** Our approach shifts decision-making to the edge by filtering video locally and sending only meaningful motion-based snippets to the cloud. Rather than continuously uploading footage, the system selectively transmits exact frames or short clips for AI analysis, significantly reducing cloud usage and cost while maintaining useful detection accuracy. Unlike traditional smart camera systems that rely on constant cloud streaming, this project emphasizes edge filtering that prioritizes cloud usage only when meaningful events occur to reduce unnecessary costs.

* **Effects:** If successful, the system will reduce data storage and cloud processing costs for individuals and organizations, making intelligent video monitoring more affordable. It also improves usability by allowing users to review only relevant events instead of hours of uneventful footage.

---

* **Use Cases (Functional Requirements):**

Use Case 1: Filtered Security Monitoring (Ethan Short)
* Actors: Homeowner (Primary), Camera (Hardware), AWS Rekognition (System).
* Triggers: Local computer detects pixel variance (motion) in the camera feed.
* Preconditions: Camera is active; Python script is running; Internet connection is stable.
* Postconditions: A filtered image is stored in AWS S3 and visible on the dashboard with a "Person" label.
* Extensions/Variations: If the label is "Animal," the system logs it but does not trigger a high-priority alert.
* Exceptions: Camera disconnected (System logs a local error); AWS API timeout (System retries upload once).

List of Steps:
1. System monitors live video feed locally.
2. System detects motion exceeding the sensitivity threshold.
3. System captures a frame and sends it to AWS Rekognition.
4. Rekognition returns "Person" label.
5. System saves the image and metadata to the Cloud Database.




Use Case 2: Wild Life Detection (Calvin Grabowski)
* Actors: Amazon Rekognition + Camera + Live video feed
* Triggers: The animals of choice that the user inputs
* Preconditions: live video feed; internet connection; long battery life or plugged in to some electricity storage; camera looks over the desired area from above; Connected to user's phone for notifications
* Postconditions: Notification sent; Video feed sent
* Extensions/Variations: Alerts can be sent to multiple accounts; Alerts can be sent in through different ways: an app, text/sms, email, etc.; If it detects any animal it would save it, not be a high prior
* Exceptions: Camera cannot see the animal (in the dark with no light); Camera's vision gets blocked (perhaps a leaf falls on it)

List of steps:
1. Live feed is running
2. Animal walks in frame
3. Camera clips the motion and sends to amazon Rekognition services
4. Animal is recognized and clip is saved
5. User is notified


---
* **Non-functional Requirements:**
1. Latency: The time from motion detection to the cloud-processed label appearing on the dashboard should be under 10 seconds.
2. Usability: The web dashboard must be responsive and viewable on both desktop and mobile browsers.
3. Efficiency: The local Python application should consume less than 15% of the CPU on a standard laptop to ensure it can run in the background.

* **External Requirements:**
1. AWS Connectivity: The system requires a stable internet connection to communicate with AWS S3 and Rekognition.
2. Hardware: A 720p or higher USB webcam or integrated laptop camera is required for sufficient image clarity for AI analysis.
3. API Limits: The system must stay within the AWS Free Tier or the user’s specified budget for Rekognition API calls.

* **Technical Approach:** A local Python application performs motion detection on a webcam feed and captures only significant movement using frame differences. When the frames change the frames will be pinged. These frames are uploaded to AWS S3, processed by an AWS Lambda function using Amazon Rekognition, and displayed through a web-based dashboard with optional real-time alerts via AWS SNS.

* **Risks:** The most significant risk is inaccurate motion detection at the edge, which could cause unnecessary uploads or missed events. This will be mitigated through adaptive motion thresholds, background subtraction, and filtering to ensure that only meaningful motion triggers cloud processing.

* **Team Roles & Justification**
  * Ethan Short (Cloud Lead): Responsible for AWS architecture and Database integrity. Chosen for ability to manage secure API keys and cloud permissions.
  * Calvin Grabowski (Motion Lead): Responsible for the "Edge" logic. Chosen for interest in computer vision and local Python optimization.
  * Michael Wilde (Integration Lead): Responsible for connecting the Edge to the Cloud and UI. Chosen for full-stack experience and AWS SDK familiarity.
  * Samuel Dressel (Optimization Lead): Responsible for filtering logic and noise reduction. Chosen for focus on software robustness and reducing "False Positives."

* **Time Line:**
### Phase 1: Foundation & Infrastructure (Weeks 1-3)
#### Week 1 (Jan 12 - Jan 18)
Goal: Repository setup and initial motion prototyping.
- [ ] Calvin: Implement basic OpenCV frame-differencing script that saves a .jpg locally when motion is detected.
- [ ] Ethan: Set up AWS account and IAM users with S3/Rekognition permissions for all team members.

#### Week 2 (Jan 19 - Jan 25)
Goal: Class presentation and Cloud connectivity.
- [ ] Michael: Create a Python script using boto3 that successfully uploads a test file to an S3 bucket.
- [ ] Samuel: Implement a "Cooldown" timer in the local script to prevent 100 images from being captured in 1 second.

#### Week 3 (Jan 26 - Feb 1)
Goal: First "End-to-End" test (Local to Cloud).
- [ ] Ethan: Integrate the S3 upload script into the motion detection loop.
- [ ] Calvin: Create an AWS Lambda trigger that runs whenever a new image hits the S3 bucket.

### Phase 2: Core Intelligence (Weeks 4-6)
#### Week 4 (Feb 2 - Feb 8)
Goal: AI Labeling.
- [ ] Michael: Write the Lambda function code to call Amazon Rekognition and print detected labels to the console.
- [ ] Samuel: Research and implement "Background Subtraction" (MOG2) to improve motion accuracy over simple differencing.

#### Week 5 (Feb 9 - Feb 15)
Goal: Database & Dashboard Start.
- [ ] Calvin: Set up a DynamoDB table to store metadata (Timestamp, S3 URL, AI Labels).
- [ ] Ethan: Create a basic Flask or React frontend that displays a "Hello World" list of items from DynamoDB.

#### Week 6 (Feb 16 - Feb 22)
Goal: Dashboard Visualization.
- [ ] Michael: Build the UI component to display the actual captured images alongside their AI tags.
- [ ] Samuel: Add "Sensitivity" sliders to the local Python app to allow user-defined motion thresholds.

### Phase 3: Optimization & Delivery (Weeks 7-9)
#### Week 7 (Feb 23 - Mar 1)
Goal: Cost Savings Logic.
- [ ] Calvin: Implement the "Cost-Savings Calculator" logic by tracking "Frames Skipped" vs "Frames Sent."
- [ ] Ethan: Conduct robustness testing: disconnect internet during capture and verify the system doesn't crash.

#### Week 8 (Mar 2 - Mar 8)
Goal: Stretch Goals & Refinement.
- [ ] Michael: (Stretch Goal) Implement AWS SNS to send a text message when the "Person" label is detected.
- [ ] Samuel: Perform a 1-hour "Live Run" to find bugs and document them as "Risks/Mitigations" in the final report.

#### Week 9 (Mar 9 - Mar 15)
Goal: Final Documentation & Video Demo.
- [ ] Entire Team: Complete the README.md with installation instructions.
- [ ] Entire Team: Finalize the living document and record a 5-minute project demo video.

## Major Features
* Local Motion "Gatekeeper": A Python application that reads a webcam feed and successfully filters out static backgrounds, triggering only on significant movement.
* Cloud Integration Pipeline: Automatic secure upload of captured frames to an AWS S3 bucket using the Boto3 SDK.
* AI Analysis Service: A backend Lambda function that processes uploaded images via Amazon Rekognition and returns a list of detected labels (e.g., Person, Car, Pet).
* Event Dashboard: A web-based user interface that displays a list of recent detections, showing the timestamp, the image, and the tags returned by the AI.

## Stretch Goals
* Cost-Savings Calculator: A visualization on the dashboard comparing "Estimated Cost if Full Streaming" vs. "Actual Cost with EdgeGuard," using live AWS pricing data.
* SMS/Email Alerts: Integration with AWS SNS (Simple Notification Service) to text the user immediately when a specific "High Threat" object (e.g., a person at night) is confirmed by the cloud.

## Other Ideas
* Running app: Make a running app that allows the user to help make workout paces for the user based on what they want to do. This would be useful with all runners by making it easier for people with different paces to get the exact pace that they should be running
* Guitar Idea: Make an ai that reads music and writes it into the app. Then the app would have recorded videos of each note on a guitar to help with fingering. It would play a clip of ethan playing the guitar at each note when the note hits. You can change tempo, and it would play the song with clips of Ethan playing combined
* Motion Detection: check to see movement in frames, and then send it to amazon to figure out what moved, and provide a cheaper process than others availiable
* Worship night: have an app to help work with schedules and visualize who is playing what on what day
* Losing Tickets: make a system that fixes that by making a better ticketing system with an interface that connects to a new ticket system that makes it easier to track status on a ticket, and what computers are linked to the ticket, and who is working on the ticket.
