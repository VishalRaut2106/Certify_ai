import webview
import threading
import uvicorn
import time
import requests
import sys
import os

# Import the FastAPI app
from app import app

def run_server():
    """Run the FastAPI server in a background thread."""
    # We use a fixed port for simplicity, or could use an ephemeral port
    uvicorn.run(app, host="127.0.0.1", port=8123, log_level="error")

def check_server_ready():
    """Wait for the server to be ready before showing the webview."""
    for _ in range(30):
        try:
            response = requests.get("http://127.0.0.1:8123/")
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    return False

def on_closed():
    """Handle window close event."""
    # System exit will kill the daemon thread
    os._exit(0)

if __name__ == '__main__':
    # Start the server in a daemon thread so it exits when the main thread exits
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for the server to be responsive
    if not check_server_ready():
        print("Error: Could not start the backend server.")
        sys.exit(1)

    # Create and start the webview window
    window = webview.create_window(
        'CertifyAI - Certificate Verification',
        'http://127.0.0.1:8123/',
        width=1200,
        height=800,
        min_size=(800, 600)
    )
    
    window.events.closed += on_closed
    
    webview.start()
