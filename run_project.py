import subprocess
import sys
import os

def run():
    print("Syncing dependencies...")
    # Update Python deps
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "src/requirements.txt", "--quiet"])
    
    # Update NPM deps
    frontend_path = os.path.join(os.getcwd(), "edgeguard-frontend")
    if os.path.exists(frontend_path):
        subprocess.run(["npm", "install", "--quiet"], cwd=frontend_path, shell=(os.name == 'nt'))

    print("Launching EdgeGuard...")

    # Start Frontend (Background)
    # shell=True is needed for Windows to find npm
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "4321"], 
        cwd=frontend_path, 
        shell=(os.name == 'nt')
    )

    print("Initializing Camera Feed (Ctrl+C to stop)...")
    try:
        # Start Backend (Foreground)
        subprocess.run([sys.executable, "-m", "src.motion_detection"])
    except KeyboardInterrupt:
        print("\nStopping EdgeGuard...")
    finally:
        frontend_proc.terminate()
        print("Shutdown complete.")

if __name__ == "__main__":
    run()