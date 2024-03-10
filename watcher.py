import subprocess
import sys
import os
import time
from multiprocessing import Process
from constants import ignored_files

class Watcher:
    def __init__(self):
        self.files = {}
        self.run_server()

    def run_server(self):
        try:
            subprocess.run([sys.executable, "server.py"])
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping the server...")

    def get_file_modified_times(self):
        # get all files, whether on current level or in subdirectories, skip the files in ignored_files
        all_but_ignored_files = [os.path.join(root, file) for root, dirs, files in os.walk('.') for file in files if file not in ignored_files and not any(ignored_file in os.path.join(root, file) for ignored_file in ignored_files)]
        return {
            filename: os.path.getmtime(filename) for filename in all_but_ignored_files
        }

    def monitor_changes(self):
        try:
            while True:
                time.sleep(1)  # Check for changes every second
                new_files = self.get_file_modified_times()
                if new_files != self.files:
                    print("Changes detected, restarting server...")
                    self.files = new_files
                    # Start the server in a separate process
                    p = Process(target=self.run_server)
                    p.start()
        except KeyboardInterrupt:
            print('Terminating watcher')
            exit(0)
