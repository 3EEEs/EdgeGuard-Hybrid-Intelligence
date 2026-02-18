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
    python venv -m env
    ```
  - **Run Envrionment:**
    
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
