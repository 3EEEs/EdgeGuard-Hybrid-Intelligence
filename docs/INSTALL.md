# It is highly recommended to use a virtual environment
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

# TODO::::

### Environment File

Due to security reasons we created an environment file that won't be pushed to github. This is because it costs money for 

# TODO:::: ETHAN MAKE THE ENVIRONMENT FILE


---

After the environment is running we want to install npm if not already installed

 ```bash
npm install
 ```


# Run Front and backend together

 ### Windows Powershell (Quickest Way)

* Everytime you want to run the project in **Windows** there is a python script that updates dependencies and then runs. This will take longer the first time it is ran, because it will be installing all the requirements

  ```bash
  python run_project.py
  ```

To see the website after running the frontend navigate to http://localhost:4321

## Otherwise, if you are unable to run the program with run_project.py

### To install dependencies independently
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

To see the website after running the frontend navigate to http://localhost:4321


#### Caution

* Our program runs your computer's default camera
  
* If you have your computer connected to any outside cameras be aware if the computer sets it as default

* Likewise if you are on a mac the computer could connect to your phone and use that camera instead. This can be disallowed in the mac's settings, or can be used if you want to record through an iphone


