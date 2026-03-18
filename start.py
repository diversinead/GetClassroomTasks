import subprocess
import sys
import os
import time
import webbrowser

BASE = os.path.dirname(os.path.abspath(__file__))

print("Starting server (port 8080)...")
server = subprocess.Popen([sys.executable, os.path.join(BASE, 'server.py')])

time.sleep(1)

print("Opening launcher...")
webbrowser.open('http://localhost:8080/')

print("\nServer running. Press Ctrl+C to stop.\n")
try:
    server.wait()
except KeyboardInterrupt:
    print("\nStopping server...")
    server.terminate()
