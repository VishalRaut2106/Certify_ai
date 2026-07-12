"""
CertifyAI Simple Desktop Launcher
Opens the app in default browser - no WebView2 needed
"""
import uvicorn
import webbrowser
import time
import threading
import sys
import os

# Resolve paths for frozen exe
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    sys.path.insert(0, BASE_DIR)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PORT = 5199
URL = f'http://127.0.0.1:{PORT}'

def open_browser():
    """Wait for server, then open browser"""
    time.sleep(3)
    webbrowser.open(URL)

def main():
    print("=" * 60)
    print("  CertifyAI - Certificate Verification System")
    print("=" * 60)
    print(f"\n✓ Starting server on {URL}...")
    print("✓ Browser will open automatically...")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start server
    from app import app
    uvicorn.run(app, host='127.0.0.1', port=PORT, log_level='error')

if __name__ == '__main__':
    main()
