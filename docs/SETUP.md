### How to Setup the Software
1. Make sure the environment is running
   - **Linux/MacOS:**
    ```bash 
    source env/bin/activate
    ```
    - **Windows:**
     ```bash 
    ./env/Scripts/activate
    ```

2. Navigate to the root directory of the project
```bash
cd ~/EdgeGuard-Hybrid-Intelligence
```
3. Choose one of the following options:

**Option A — Run frontend and backend together**

```bash
python run_project.py
```
**Option B — Run frontend and backend in separate terminals**

- Terminal 1 (frontend, start in the root directory):
  ```bash
  cd edgeguard-frontend
  npm run dev
  ```
- Terminal 2 (backend, start in the root directory):
  ```bash
  python -m src.motion_detection
  ```

Once running, open your browser and navigate to http://localhost:4321 to view the dashboard.
