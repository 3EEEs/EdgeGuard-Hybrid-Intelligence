# EdgeGuard Hybrid Intelligence

**Team:** Ethan Short, Calvin Grabowski, Michael Wilde, Sammuel Dressel
**Course:** CS 362 - Software Engineering II  
**Term:** Winter 2026

## Project Overview

**EdgeGuard Hybrid Intelligence** is an automated image detection application designed to streamline video monitoring by filtering out irrelevant motion at the "edge" (locally) before sending data to the cloud.

Most current video surveillance systems rely on continuous recording or full video streaming to the cloud, resulting in high storage costs and excessive processing fees. Our solution shifts decision-making to the local device. By integrating motion-triggered capture with **Amazon Rekognition**, the system identifies specific entities (such as people, animals, or objects) and ignores environmental noise.

### [Living Document](https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence/blob/main/LIVINGDOC.md)

### Core Goals
1.  **Cost Reduction:** Minimize cloud storage and processing fees by only transmitting exact frames or short clips of relevant motion.
2.  **Efficiency:** Reduce the time users spend reviewing raw footage by providing actionable, filtered data.
3.  **Accuracy:** Use AI analysis to distinguish between significant events and background noise.

---

## Team Members & Roles

| Name | Role | GitHub Username |
| :--- | :--- | :--- |
| **Ethan Short** | Motion Detection Lead | 3EEEs |
| **Calvin Grabowski** | API & Cloud Interaction Lead | CalvinGrabowski |
| **Michael Wilde** | Video Processing Lead | LegendaryGitHub |
| **Samuel Dressel** | Motion Detection & Storage Optimization Lead | Voidless-Void |





---

## Technical Approach

Our system utilizes a hybrid local-cloud architecture:

1.  **Local "Gatekeeper" (Python):** A local application monitors a webcam feed. It uses adaptive motion thresholds and background subtraction to filter out static scenes, capturing only significant movement.
2.  **Cloud Ingestion (AWS S3):** captured frames are securely uploaded to an AWS S3 bucket using the Boto3 SDK.
3.  **AI Analysis (AWS Lambda & Rekognition):** An AWS Lambda function triggers upon upload, processing the image via Amazon Rekognition to detect labels (e.g., "Person", "Car").
4.  **User Dashboard:** A web-based interface displays recent detections, timestamps, and AI-generated tags.

### Key Features
* **Local Motion Filtering:** Prevents empty footage from reaching the cloud.
* **Cloud Integration Pipeline:** Automatic, secure upload to AWS.
* **Event Dashboard:** Visual interface for reviewing detected events.

---

## Repository Layout

This repository is organized as follows:

* **`/src`** Contains the source code for the project, including the local Python motion detection scripts and AWS Lambda function code.
    
* **`/docs`** Contains project documentation, including the Project Proposal, Requirements Elicitation, and architecture diagrams.

* **`/reports`** Contains the weekly status reports for the project. These are named by date (e.g., `20260120.md`) and detail our team's progress, individual contributions, and upcoming goals.

* **`/tests`** Contains unit tests and test scripts to ensure system reliability.

---

## Getting Started

*(Instructions for setting up the development environment will be added here as the project infrastructure is built out, e.g., `pip install -r requirements.txt`).*
