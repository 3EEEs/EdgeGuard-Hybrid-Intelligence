# Project Proposal: EdgeGuard Hybrid Intelligence
## Date: January 19, 2026 Course: CS 362


### Team Info
* Ethan Short – Cloud Lead
* Calvin Grabowski – Motion Lead
* Michael Wilde – Integration Lead
* Samuel Dressel – Optimization Lead

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


## 1. Software architecture


EdgeGuard Hybrid Intelligence uses a hybrid between edge (motion) detection and cloud implimentation, creating an event-driven architecture. The system performs early-stage motion detection and filtering **locally** at the edge, while delegating object recognition, storage, and user-facing services to cloud-based components. This architecture reduces bandwidth usage, cloud processing costs, and unnecessary data storage compared to traditional continuous-stream surveillance systems which are constantly sending the cloud meaningless updates.

The system follows a separation-of-concerns approach: motion detection, cloud processing, data persistence, and presentation are implemented as distinct components with well-defined interfaces. This allows costs to be distinct which results in not paying for things that we aren't currently using. 


> **KEY INFORMATION:** S3 is the storage (Simple Storage Service), Lambda is the short lived code that triggers events, Rekognition is the amazon AI recognition system, DynamoDB is the noSQL database, and edge is the framwork that we are going to make to capture the motion.

### 1.1 Major Software Components

#### Edge Motion Processing Component
- Local Python application monitoring a live camera feed
- Detects motion using frame differencing and background subtraction
- Applies sensitivity thresholds, cooldown timers, and zone-based rules
- Captures and uploads only relevant frames or short clips

#### Cloud Ingestion and Processing Component
- Amazon S3 stores uploaded frames from the edge
- AWS Lambda functions are triggered by S3 upload events
- Lambda functions coordinate AI analysis and filtering logic

#### AI Analysis Component
- Amazon Rekognition performs label detection on uploaded images
- Returns detected objects (e.g., Person, Car, Animal) with confidence scores
- Results are used to classify events as relevant or non-relevant

#### Data Storage Component
- Amazon DynamoDB stores metadata for detected events
- Stores references to images rather than raw image data

#### Presentation and Notification Component
- Web-based dashboard displays detection results
- Optional notifications are sent via AWS SNS for high-priority events

### 1.2 Interfaces Between Components

- **Edge → Cloud Interface**
  - HTTPS-based uploads using the AWS Boto3 SDK
  - Data transferred: filtered images and minimal metadata

- **S3 → Lambda Interface**
  - Event-driven trigger on object upload
  - Decouples ingestion from processing

- **Lambda → Rekognition Interface**
  - AWS SDK calls referencing images stored in S3

- **Lambda → DynamoDB Interface**
  - Writes structured metadata records for later querying

- **Dashboard → DynamoDB / S3 Interface**
  - Reads event metadata from DynamoDB
  - Retrieves images on demand using S3 URLs


### 1.3 Data Storage and Organization

The system minimizes local storage and does not retain full video recordings.

#### Local Storage
- Temporary in-memory buffers used during motion analysis
- No persistent video storage

#### Cloud Storage

- **Amazon S3 (Simple Storage System)**
  - Stores filtered images or short clips
  - Organized by date and event type

- **Amazon DynamoDB**

  High-level schema:
  - Primary key for DynamoDB to store data: `EventID` (for finding the event)
  - When it happened: `Timestamp`
  - Where the image is stored: `S3_Object_URL`
  - What was detected: `Detected_Labels`
  - How confident are we about what we detected: `Confidence_Scores`
  - How important is that event: `Event_Priority`
  - Where it happened: `Zone`

This design separates large binary objects from structured metadata to improve scalability and query performance.


### 1.4 Architectural Assumptions

- Edge devices have sufficient computational capacity for real-time motion detection
- Network connectivity is available for cloud-based analysis
- Users prioritize reduced cost and filtered results over full continuous video storage
- AWS services are available and properly configured
- Event-driven latency under 10 seconds is acceptable for the use cases


### 1.5 Architectural Decisions and Alternatives

#### Decision 1: Edge-Based Motion Filtering

**Chosen:** Perform motion detection locally before uploading data.

**Alternative:** Continuously stream video to the cloud for processing.

- **Pros of chosen approach**
  - Reduced cloud costs
  - Lower bandwidth usage
  - Improved privacy

- **Cons**
  - Increased processing requirements on the edge device


#### Decision 2: Serverless Cloud Processing

**Chosen:** Use AWS Lambda for event-driven processing.

**Alternative:** Use a persistent backend server (e.g., EC2).

- **Pros of chosen approach**
  - Automatic scaling
  - Lower operational overhead
  - Cost efficiency

- **Cons**
  - Cold-start latency
  - Execution time limits

---


## 2. Software design
## 3. Coding guidelines
## 4. Process description
**i. Risk assessment**
* Risk 1: Inaccurate Motion Triggering
  * Likelihood: High
  * Impact: Medium
  * Evidence: Our abstract notes on irrelevant motion, such as environmental noise, is a potential issue that can be triggered by light changes or wind and send unnecessary data to AWS Rekognition.
  * Reduction/Better Estimates: Samuel is implementing a MOG2 Background Subtraction and estimating the accuracy by running the edge script against a pre-recorded video of a static room with moving shadows. 
  * Detection: Check to see what data is being sent to AWS Rekognition.
  * Mitigation: Have a "sensitivity slider" added for the user to manually adjust sensitivity.
* Risk 2: Latency to AWS Rekognition
  * Likelihood: Medium
  * Impact: Low
  * Evidence: Our NFR specifies a less than 10-second delay for our software to process the frame.
  * Reduction/Better Estimates: Perform a "stopwatch" test from the moment that motion is detected to when all the data is processed.
  * Detection: Incorporate a "Process_Time" field in the DynamoDB schema to track the duration from Timestamp to DB_Write_Time.
  * Mitigation: If the latency is too high, investigate the "Provisioned Concurrency" for Lambda or reduce the image resolution/size before uploading to S3 to speed up transfer.
* Risk 3: AWS Free Tier Exhaustion
  * Likelihood: Medium
  * Impact: Medium
  * Evidence: Rekognition is not infinitely free, and in high-traffic areas could trigger hundreds of pings and max out the budget.
  * Reduction/Better Estimates: The "Cooldown timer" can be used as a primary defense, and it can be used to estimate monthly costs.
  * Detection: AWS Budget Alerts will be set to a max cap, and we will get notified when it's reached.
  * Mitigation: Implement the "Emergency Kill Switch" in the edge script, which stops the upload if the local count exceeds a daily limit.
* Risk 4: "Edge" Hardware & Environment Variability
  * Likelihood: Medium
  * Impact: Medium
  * Evidence: Use Case 3 mentions "daytime hours" and street zones. Performance may drop significantly at night or if the camera becomes obstructed.
  * Reduction/Better Estimates: Test the camera in three lighting conditions: Bright daylight, Indoor lighting, and Low light.
  * Detection: Low "Confidence_Scores" (below 50%) consistently appearing in DynamoDB for objects that are clearly visible to humans.
  * Mitigation: Document minimum lux (lighting) requirements in the README. If confidence is low, the system could skip the "High Priority" alert but still save the metadata for manual review.
* Risk 5: Unhandled Network Interruptions (Edge-to-Cloud Gap)
  * Likelihood: Medium
  * Impact: Medium
  * Evidence: Use Case 3 mentions "Network connections; system may fall back to local processing." If the internet drops while a frame is being sent via boto3, the Python script may hang or crash.
  * Reduction/Better Estimates: Ethan will test this in Week 7 and simulate a connection loss by disabling the connection to the internet while running the edge script.
  * Detection: Implementing a try-except block around the S3 upload function and logging the number of ConnectionError events locally.
  * Mitigation: Implement a local SQLite queue. If the upload fails, please save the metadata locally and try the upload again once the connection is restored.

**ii. Documentation**
Our current plan for the documentation style that we plan to create for our hybrid architecture is to ensure that our local Python environment and the AWS cloud infrastructure are transparent and maintainable. 
1. **Developer Documentation (Technical Reference)**
   * API & Data Contract (docs/INTERFACES.md): Since the backend is locked, this document acts as the "source of truth" for the team. It will define the structure of the JSON metadata sent to the DynamoDB and the naming conventions for S3 objects. This ensures everything can stay synced.
   * Motion Logic Technical Guide (docs/MOTION_PROCESSING.md): A write up into the "Gatekeeper" logic, which will explain the implementation of frame-differencing and background subtraction, including how to tune the sensitivity and cooldown variables within the code.
   * Local Environment Setup:
2. **User & Operator Documentation**
   * Quick-Start User Guide (docs/USER_MANUAL.md): A guide for the "Homeowner" actor. It will include instructions on camera placement, how to run the local Python script, and how to access the Web Dashboard to view filtered results.
   * Cost & Performance Optimization Guide: A section explaining the trade-offs between local "Edge" settings and AWS costs. It will teach the user how to minimize Rekognition pings by adjusting the sensitivity sliders.
   * System Health & Troubleshooting: A troubleshooting tree for common local issues, such as "Camera not detected" or "S3 Upload failed (Network Error)," including how to check the local logs
3. **Project Governance**
   * Weekly Status Reports (/reports): Ongoing documentation of the project's health, following the YYYYMMDD.md format to document the team's progress and goals.

## Use Cases (Functional Requirements):

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




Use Case 3: Filtered Street Drive-By Monitoring
* Actors: Homeowner / System User(Primary), EdgeGuard Hybrid Intelligence(System), AWS Services(System)
* Triggers: A car is detected driving by the camera’s field of view in the street zone.
* Preconditions: EdgeGuard Hybrid Intelligence is installed and operational, Available internet conection, working motion capture camera, camera is position is positioned to capture both the driveway and street zones, AWS services are linked to system and configured, User has defined street and driveway zones, daytime hours are set in the system, only drive-by vehicles are considered non-relevant, vehicle detections in the street zones are properly defined
* Postconditions: Drive-by vehicle motion in the street zone during daytime hours is classified as non-relevant, No alert is generated for the user, No long-term cloud storage is used for daytime street drive-by events
* Extensions/Variations:
  1. Vehicles that stop, enter the driveway, or linger beyond the configured time threshold are reclassified as relevant and recorded
  2. Drive-by vehicles occurring outside daytime hours are treated as relevant and recorded;
  3. Events with a person detected alongside a car are always considered relevant
  4. Changes to daytime hours or disabling vehicle filtering apply to subsequent events.
* Exceptions:
  1. A slow-moving or temporarily stopped car in the street zone is misclassified as a drive-by and filtered out
  2. An object that is not a car is incorrectly classified as a car
  3. AWS services fail, preventing proper analysis or storage
  4. Network connection fails, limiting cloud-based processing; system may fall back to local processing


List of Steps: 
1. A car drives past the camera within the street zone during configured daytime hours.
2. EdgeGuard detects motion locally in the background.
3. The system tracks the motion’s duration and trajectory.
4. The motion is classified locally as a drive-by event.
5. One or more frames are captured and uploaded to AWS S3.
6. An AWS Lambda function is triggered by the upload.
7. Amazon Rekognition analyzes the image and returns the label “Car.”
8. EdgeGuard evaluates filtering rules:
   1. Motion occurred entirely in the street zone.
   2. Time of day is within configured daytime hours.
   3. Object label is “Car.”
   4. Motion pattern matches a drive-by.
9. The event is filtered out and discarded without notifying the user.




Use Case 4: Residential/Commercial Burglary Detection (by Michael Wilde)
* Actors: Homeowner / System User(Primary), EdgeGuard Hybrid Intelligence(System), AWS Services(System)
* Triggers:  When motion is detected at a primary point of entry during the state of 'stay' or 'away' armed state.
* Preconditions: When the security system is armed (stay or away) and clear line of sight to points of entry and connected to internet for sending the data.
* Postconditions: Verify that a intruder has entered and said an alert to the owner with evidence being stored in cloud and a silent alarm can be triggered. 
* Extensions/variations:
  * Facial Recognition: Integrate face comparsion to see if the person is "Authorized" before sounding the alarm.
  * Weapon Detection: Use Rekognition to specifically scan for labels like "weapon" or crowbar" to escalate the priority of the alert.
* Exceptions:
  * Network Failure: If AWS connection is lost, system defaults to a standard motion alert without filtering.
  * Occlusion: Intruder is wearing a mask or heavy camouflage to prevent facial detection to reach a confidence threshold. 

List of Steps:
1. A camera detects motion at a restricted entry point during an armed state.
2. Application captures a burst of high-definition images to ensure clear visibility of the subject's face or clothing.
3. Images are sent to Amazon Rekognition to perform a label detection.
4. Application filters the results based on highest confidence score (above 90%).
5. Environmental Noise is checked and discards if no person is detected.
6. Application cross-references detection with the armed status of the building alert to the owner's device.
7. The filtered footage is tagged as "Critical Evidence" and moved to long-term cloud storage.  

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
