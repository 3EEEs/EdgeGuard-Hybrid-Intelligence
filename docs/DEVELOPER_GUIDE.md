# Developer Guide

## 1. Obtaining the Source Code

To obtain the EdgeGuard Hybrid Intelligence source code:

1. Clone the repository from GitHub:  
```bash
git clone https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence.git
```

2. Navigate to the file location where your last command looks like
 ```bash
cd EdgeGuard-Hybrid-Intelligence
```

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


## 2. Directory Structure

The project is organized as follows:

```bash
EdgeGuard-Hybrid-Intelligence/
│
├── code/                   # All source code (Edge + Cloud scripts)
├── docs/                   # Developer & User documentation
├── reports/                # Weekly progress reports
├── tests/                  # Unit and integration tests
├── LIVINGDOC.md            # Project proposal & living document
└── README.md               # Overview, installation, quick start

```

 

- **Source files:** `code/`  
- **Tests:** `tests/` 
- **Documentation:** `docs/`  
- **Reports:** `reports/`  
- **Data files:** Stored temporarily at edge or in AWS S3 (no persistent local storage)

---

## 3. Building the Software

EdgeGuard Hybrid Intelligence does not require compilation as it is written in **Python** and uses **serverless AWS components**.

### Local Edge (Python)
1. Ensure Python 3.10+ is installed.
2. Install required packages:
   
```bash
pip install -r code/requirements.txt
```
3. Run the main code
   
```bash
python code/motion_detection.py
```

### Cloud Components (AWS)

1. Configure AWS CLI with credentials.
   
    You have two options:  
   - **Use the project account:** Talk to Ethan to get the AWS access keys and secret keys for the team account.  
   - **Use your own AWS account:** You can create a personal AWS account and set up your own S3 bucket and Lambda functions to test the system.


2. Navigate to the AWS folder from the project root:

```bash
cd code/aws
```
3. Deploy/update Lambda functions:

```bash
./deploy.sh
```

4. Verify S3 buckets and triggers are correctly configured.
```bash
aws s3 ls
```

* Confirm that the expected bucket(s) exist (e.g., edgeguard-uploads).

* In the AWS Console, go to Lambda → Functions → [Your Function] → Triggers and make sure the S3 bucket is listed.

* Optionally, test with a sample upload:

  ```bash
  aws s3 cp sample.jpg s3://edgeguard-uploads/
  ```

## 4. Testing the Software

Testing is divided into three levels: Unit, Integration (System), and Usability.

### Local Edge Tests (Python)
To run the unit tests for the local motion detection and S3 upload modules, we use `pytest`.

1. Ensure your virtual environment is active.
2. Install testing dependencies:
   ```bash
   pip install pytest
   ```
3. Run the test suite from the root directory:
   ```bash
   pytest test/
   ```

### Cloud Integration Tests (AWS)
Because the cloud architecture is serverless, integration testing requires triggering live AWS events to verify the pipeline (S3 → Lambda → Rekognition → DynamoDB).
1. Ensure your AWS credentials are configured locally via the AWS CLI or your .env file.
2. Upload a test image to your S3 bucket to trigger the pipeline:
   ```bash
   aws s3 cp tests/sample_data/test_car.jpg s3://edgeguard-storage-short-992 /
   ```
3. Verify the execution by checking the AWS CloudWatch logs for your Lambda function, or query the DynamoDB table to ensure the metadata and AI labels were successfully written:
   ```bash
   aws dynamodb scan --table-name EdgeGuard_Events
   ```

### Web Dashboard Tests (React)
To test the presentation layer:

1. Navigate to the web application directory:
   ```bash
   cd code/dashboard
   ```
2. Run the frontend test suite (using Jest/React Testing Library):
   ```bash
   npm test
   ```

### Adding New Tests
All developers are expected to write tests for new features to ensure our edge-to-cloud pipeline remains robust.

Where to put tests: All Python tests must be placed inside the tests/ directory at the project root. React tests should be placed in code/dashboard/src/__tests__/.

Naming Conventions: * Python: Test files must start with test_ (e.g., test_motion_detector.py). Test function names inside those files must also start with test_ (e.g., def test_cooldown_timer():).

JavaScript/React: Test files should use the .test.js or .spec.js suffix (e.g., EventFeed.test.js).

Test Harness: * Use pytest for all Python modules.

Use Jest for the React Dashboard.

Mocks: When testing AWS integration locally, use the moto library to mock boto3 calls so we do not exhaust our AWS Free Tier limits during automated CI/CD runs.

## 5. Building a Release
Since EdgeGuard Hybrid Intelligence consists of an edge client, a cloud backend, and a web dashboard, releasing a new version requires a few coordinated steps. Currently, this process is manual.

Pre-Release Tasks
Update Version Numbers: Update the version number in code/VERSION.txt and inside the code/dashboard/package.json file.

Sanity Checks (End-to-End Test): Before tagging a release, a developer must perform a live system test:

Run the edge Python script locally with a live webcam.

Trigger significant motion in front of the camera.

Verify the image appears on the web dashboard within 10 seconds with the correct AI labels and confidence scores.

## 6. Deployment Tasks
Cloud Update: Package and deploy any updated Lambda functions or IAM permission changes using the AWS Console or the provided deploy script (code/aws/deploy.sh).

Dashboard Build: Compile the React application for production:

```bash
   cd code/dashboard
   npm run build
   ```
Tag the Release: Create a release tag in GitHub (e.g., v1.0.0-beta) summarizing the new features and bug fixes.

Commit this to your `main` branch and you can check off the "Developer Documentation" requirement for the assignment! 

You have less than two hours left. Would you like me to draft up the `docs/USER_MANUAL.m
