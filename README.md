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
| **Ethan Short** | API & Cloud Interaction Lead | 3EEEs |
| **Calvin Grabowski** | Motion Detection Lead | CalvinGrabowski |
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
# EdgeGuard Hybrid Intelligence

**Team:** Ethan Short, Calvin Grabowski, Michael Wilde, Samuel Dressel  
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
| **Ethan Short** | API & Cloud Interaction Lead | 3EEEs |
| **Calvin Grabowski** | Motion Detection Lead | CalvinGrabowski |
| **Michael Wilde** | Video Processing Lead | LegendaryGitHub |
| **Samuel Dressel** | Motion Detection & Storage Optimization Lead | Voidless-Void |

---

## Technical Approach



Our system utilizes a hybrid local-cloud architecture:

1.  **Local "Gatekeeper" (Python):** A local application monitors a webcam feed. It uses adaptive motion thresholds and background subtraction to filter out static scenes, capturing only significant movement.
2.  **Cloud Ingestion (AWS S3):** Captured frames are securely uploaded to an AWS S3 bucket using the Boto3 SDK.
3.  **AI Analysis (AWS Lambda & Rekognition):** An AWS Lambda function triggers upon upload, processing the image via Amazon Rekognition to detect labels (e.g., "Person", "Car").
4.  **User Dashboard:** A web-based Astro/React interface displays recent detections, timestamps, and AI-generated tags.

### Key Features
* **Local Motion Filtering:** Prevents empty footage from reaching the cloud.
* **Cloud Integration Pipeline:** Automatic, secure upload to AWS.
* **Event Dashboard:** Visual interface for reviewing detected events.

---

## Repository Layout

This repository uses a monorepo structure to separate the distinct software components:

* **`/edge-client`**: Contains the local Python computer vision scripts (OpenCV) and AWS upload logic.
* **`/cloud-backend`**: Contains the AWS Lambda functions and Rekognition logic.
* **`/web-frontend`**: Contains the Astro/React code for the user dashboard.
* **`/docs`**: Contains project documentation, including the Project Proposal, API contracts, and architecture diagrams.
* **`/reports`**: Contains our weekly status reports detailing progress and goals.
* **`/tests`**: Contains our automated test suites.
* **`/beta-testing`**: Contains feedback reports generated by our classmates.

---

## Operational Use Cases (Beta Release)

Currently, **Use Case 1: Filtered Security Monitoring** is fully operational end-to-end. 
* The local Python script detects motion and uploads the frame to AWS S3.
* AWS Lambda is triggered and processes the image via Amazon Rekognition.
* The React/Astro web dashboard fetches and displays the filtered event data.
---

## Getting Started

### Prerequisites
To run this project locally, your machine must have the following installed:
* **Python 3.10+**
* **Node.js 18+** & **npm**
* **AWS CLI** (Configured with credentials provided by the team for beta testing)
* A working webcam (built-in or USB)

### 1. Build & Installation Instructions

Because this is a hybrid architecture, you need to install dependencies for both the local edge client and the web frontend.

**A. Edge Motion Client (Python)**
Open your terminal and navigate to the edge client directory:
cd edge-client
# It is highly recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install required Python packages (OpenCV, Boto3, etc.)
pip install -r requirements.txt

B. Web Dashboard (Astro/React)
Open a new terminal window and navigate to the frontend directory:

Bash
cd web-frontend

# Install Node modules
npm install
2. Running the System
To see the full system work, you need to run the web dashboard and the edge camera script simultaneously.

Step 1: Start the Web Dashboard
In your web-frontend terminal, start the development server:

cd web-frontend
npm run dev
Open your browser and navigate to http://localhost:4321 to view the dashboard.

Step 2: Start the Edge Camera
In your edge-client terminal (with your virtual environment activated), run the main script:

cd edge-client
python main.py
A webcam window will open. Move in front of the camera to trigger the motion detection. Check the web dashboard to see your captured frame appear!

3. Testing the System
We have automated testing set up for both the Python backend and the JavaScript frontend.

Running Python Unit Tests (Edge/Cloud)

cd edge-client
pytest
Running Frontend Linting & Build Tests

cd web-frontend
npm run lint
npm run build


# Running Backend

3. Create an environment
  
  #### Windows Powershell
  - **Create enviroment (optional):**
    
    ```bash 
    python -m venv env 
    ```
  - **Run Environment:**
    
    ```bash 
    ./env/Scripts/activate
    ```

  #### Linux/macOS 
  - **Create enviroment (optional):**

    ```bash 
    python3 -m venv env
    ```
  - **Run Envrionment:**
    
    ```bash 
    source env/bin/activate
    ```

### Local Edge (Python)
1. Ensure Python 3.10+ is installed.
2. Install required packages:
   
```bash
pip install -r code/requirements.txt
```
3. Run the main code
   
```bash
python -m src.motion_detection
```
