# First clone the repository

Here is a link to the [Repository](https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence/tree/main) if wanted.

Go in a terminal or IDE terminal and clone the repository into the location you wish to have it

```bash
git clone git@github.com:3EEEs/EdgeGuard-Hybrid-Intelligence.git
```

Then enter the directory

```bash
cd .\EdgeGuard-Hybrid-Intelligence\
```

we will refer to this location as the main directory.

# It is highly recommended to use a virtual environment

### Prerequisites
To run this project locally, your machine must have the following installed:
* **Python 3.10+**
* **Node.js 18+**
* A working webcam (built-in or USB)

### 1. Build & Installation Instructions
  
  Here are instructions on how to create and run an environment on either Windows Powershell or Linux. All of these are done in the main project folder.

  #### Windows Powershell
  
  - **Create enviroment (optional):**
    
    ```bash 
    python -m venv env 
    ```
  - **Start Environment:**
    
    ```bash 
    ./env/Scripts/activate
    ```

  #### Linux/macOS 
  - **Create enviroment (optional):**

    ```bash 
    python3 -m venv env
    ```
  - **Start Envrionment:**
    
    ```bash 
    source env/bin/activate
    ```

After you have your environment set up, you only have to start the environment when you come back, you only create the environment when you intially need it for your own device.

### AWS setup

Use these credentials in the Environment file below

### Environment File

Due to security reasons we created an environment file that won't be pushed to github this is a read only file! Your environemt should be in the root folder and look like the below

Access Key:
AKIAUTXMQSD7BBT3JQYN

Secret Access Key:
7rdhf6q2+aD8HVKwDgLEUvpaBegmTOtzjrc1rIaL7rdhf6q2+aD8HVKwDgLEUvpaBegmTOtzjrc1rIaL

#### EdgeGuard Beta Test Credentials (.env)
```
AWS_ACCESS_KEY_ID=PASTE_TEST_KEY_HERE
AWS_SECRET_ACCESS_KEY=PASTE_TEST_SECRET_HERE
AWS_REGION=us-west-2
S3_BUCKET_NAME=edgeguard-storage-short-992
```

---

After the environment is running we want to install npm if not already installed

 ```bash
npm install
 ```


# Run Front and backend together

 ### Windows Powershell and Linux (if python is fully installed) (Quickest Way to run the software)

* Everytime you want to run the project in **Windows** there is a python script that updates dependencies and then runs. This will take longer the first time it is ran, because it will be installing all the requirements

  ```bash
  python run_project.py
  ```

To see the website after running the frontend navigate to http://localhost:4321 because it is hosted by the individual computer.

## Otherwise, if you are unable to run the program with run_project.py

### Install dependencies independently
1. Ensure Python 3.10+ is installed.
2. Install required packages:
   
```bash
pip install -r src/requirements.txt
```

 ```bash
npm install
 ```

## If you want to run them independently

To see the full system work, you need to run the web dashboard and the edge camera script simultaneously on different terminals.

1. **Terminal 1:** Run the frontend (start in the main folder)
```bash
cd edgeguard-frontend
npm run dev
```

2. **Terminal 2:** Run the backend (start in the main folder)
```bash
python -m src.motion_detection
```

To see the website after running the frontend navigate to http://localhost:4321 because it is hosted by the individual computer.


#### Caution

* Our program runs your computer's default camera
  
* If you have your computer connected to any outside cameras be aware if the computer sets it as default

* Likewise if you are on a mac the computer could connect to your phone and use that camera instead. This can be disallowed in the mac's settings, or can be used if you want to record through an iphone


