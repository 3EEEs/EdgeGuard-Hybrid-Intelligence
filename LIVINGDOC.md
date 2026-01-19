# Project Proposal: EdgeGuard Hybrid Intelligence
## Date: January 13, 2026 Course: CS 362


### Team Info
* Ethan Short – Motion Detection Lead
* Calvin Grabowski – API and Cloud Integration Lead
* Michael Wilde – Video Processing Lead
* Samuel Dressel – Motion Detection and Storage Optimization Lead


## Project Artifacts

Code Repository: [Link](https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence)

Project Board: [Github Project](https://github.com/users/3EEEs/projects/2/views/1)

Google Doc: [Project Deliverable 1](https://docs.google.com/presentation/d/1xFujLNTsQRAWX66ZN-khSHP7Vj1CQskHdH3TL1hhviU/edit)

## Communication Plan

Channels: Discord and text groupchat for daily synchronous chat; GitHub Issues for task tracking; Weekly meeting after class and as needed.

## Rules:
* All code changes must go through a Pull Request with at least one review.
* "Blockers" must be communicated in Discord immediately.
* Response time expectation: Within 24 hours on weekdays.

## Product Description

* **Abstract:** This project introduces an automated image detection application designed to streamline video monitoring by filtering out irrelevant motion. By integrating motion-triggered capture with Amazon Rekognition, the system identifies specific entities (such as people, animals, or objects) and ignores environmental noise. This solution reduces the time spent reviewing raw footage and provides businesses with actionable, filtered data, ultimately lowering operational costs and improving security efficiency.

* **Goal:** Takes snippets of movement from a video and saves those snippets. This saves total storage, saves money by making our customers not having to submit as much to amazon rekognition, and it makes it easier for humans to go through the snippets. Our product would send only exact frames or small clips to amazon rekognition to save money, by sending less frames than other services and less expensive than other options.

* **Current Practice:** Most video surveillance and monitoring systems rely on continuous recording or full video streaming to the cloud, where all footage is stored and analyzed. This approach results in high storage costs, excessive cloud processing fees, and large volumes of irrelevant footage that users must manually review.

* **Novelty:** Our approach shifts decision-making to the edge by filtering video locally and sending only meaningful motion-based snippets to the cloud. Rather than continuously uploading footage, the system selectively transmits exact frames or short clips for AI analysis, significantly reducing cloud usage and cost while maintaining useful detection accuracy.

* **Effects:** If successful, the system will reduce data storage and cloud processing costs for individuals and organizations, making intelligent video monitoring more affordable. It also improves usability by allowing users to review only relevant events instead of hours of uneventful footage.

* **Use Cases (Functional Requirements):**

* **Non-functional Requirements:**

* **External Requirements:**

* **Technical Approach:** A local Python application performs motion detection on a webcam feed and captures only significant movement. These frames are uploaded to AWS S3, processed by an AWS Lambda function using Amazon Rekognition, and displayed through a web-based dashboard with optional real-time alerts via AWS SNS.

* **Risks:** The most significant risk is inaccurate motion detection at the edge, which could cause unnecessary uploads or missed events. This will be mitigated through adaptive motion thresholds, background subtraction, and filtering to ensure that only meaningful motion triggers cloud processing.

* **Time Line:**
  

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
