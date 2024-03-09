import subprocess
import sys
import os
import time
from multiprocessing import Process

ignored_files = ['main.py', '.git', 'venv', '.idea']

def run_server():
    subprocess.run([sys.executable, "server.py"])

def get_file_modified_times():
    return {
        filename: os.path.getmtime(filename)
                for filename in os.listdir('.')
                if filename not in ignored_files
    }

def monitor_changes():
    files = {}
    try:
        while True:
            time.sleep(1)  # Check for changes every second
            new_files = get_file_modified_times()
            if new_files != files:
                print("Changes detected, restarting server...")
                files = new_files
                # Start the server in a separate process
                p = Process(target=run_server)
                p.start()
    except KeyboardInterrupt:
        print('Terminating watcher')
        exit(0)

if __name__ == "__main__":
    monitor_changes()
