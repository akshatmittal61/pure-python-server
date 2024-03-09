import subprocess
import sys
import os
import time
from multiprocessing import Process

ignored_files

def run_server():
    subprocess.run([sys.executable, "main.py"])

def get_file_modified_times():
    return {filename: os.path.getmtime(filename) for filename in os.listdir('.') if filename not in ['main.py', '.git', 'venv', '.idea']}

def monitor_changes():
    files = {}
    try:
        while True:
            time.sleep(1)  # Check for changes every second
            new_files = get_file_modified_times()
            if new_files != files:
                print(files, new_files)
                print("Changes detected, restarting server...")
                files = new_files
                # Start the server in a separate process
                p = Process(target=run_server)
                p.start()
                p.join()  # Wait for the server process to complete
    except KeyboardInterrupt:
        print('Terminating watcher')
        exit(0)

if __name__ == "__main__":
    monitor_changes()
