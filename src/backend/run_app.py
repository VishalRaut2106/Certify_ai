"""
Simple launcher for CertifyAI app
Starts FastAPI server and opens browser
"""
import uvicorn
import webbrowser
import time
import threading

PORT = 5199
URL = f'http://127.0.0.1:{PORT}'

def open_browser():
    """Wait for server to start, then open browser"""
    time.sleep(2)  # Give server time to start
    webbrowser.open(URL)
    print(f"\n✓ Browser opened at {URL}")
    print("✓ Press Ctrl+C to stop the server")

if __name__ == '__main__':
    print("=" * 50)
    print("  CertifyAI - Certificate Verification")
    print("=" * 50)
    print(f"\nStarting server on {URL}...")
    
    # Start browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start server (blocks until Ctrl+C)
    from app import app
    uvicorn.run(app, host='127.0.0.1', port=PORT, log_level='info')
