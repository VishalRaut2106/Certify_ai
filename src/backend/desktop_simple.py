"""
CertifyAI Simple Desktop Launcher
Opens the app in default browser and displays application terminal
"""
import io
import sys
import os
import time
import threading
import webbrowser
import urllib.request
import uvicorn

# Stream fallback in case console is unavailable
class NullStream(io.TextIOBase):
    def write(self, s):
        return 0
    def flush(self):
        pass
    def isatty(self):
        return False

if sys.stdout is None:
    sys.stdout = NullStream()
if sys.stderr is None:
    sys.stderr = NullStream()
if sys.stdin is None:
    sys.stdin = NullStream()

# Resolve paths for frozen exe
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    sys.path.insert(0, BASE_DIR)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PORT = 5199
URL = f'http://127.0.0.1:{PORT}'

def check_existing_instance():
    """Check if server is already running on PORT; if so, open browser and exit secondary launcher."""
    try:
        req = urllib.request.urlopen(f'http://127.0.0.1:{PORT}/', timeout=1)
        if req.status == 200:
            print("=" * 60)
            print(f"  [INFO] CertifyAI is ALREADY running on {URL}")
            print("  [INFO] Re-opening web browser window...")
            print("=" * 60)
            webbrowser.open(URL)
            time.sleep(1.5)
            sys.exit(0)
    except Exception:
        pass  # No server running yet, proceed to startup

def create_desktop_shortcut():
    """Create a desktop shortcut if it doesn't exist and we are running as an exe"""
    if not getattr(sys, 'frozen', False):
        return  # Only create shortcut for the built .exe
        
    import subprocess
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    shortcut_path = os.path.join(desktop, 'CertifyAI.lnk')
    
    if not os.path.exists(shortcut_path):
        exe_path = sys.executable
        # Use PowerShell to create the shortcut using Windows COM objects
        ps_script = f'''
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{exe_path}"
        $Shortcut.Description = "CertifyAI Verification System"
        $Shortcut.Save()
        '''
        try:
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print(f"✓ Created Desktop Shortcut for easy access")
        except Exception as e:
            print(f"Failed to create shortcut: {e}")

def open_browser():
    """Wait for server, then open browser"""
    create_desktop_shortcut()
    time.sleep(2)
    webbrowser.open(URL)

def main():
    # 1. Check for single instance on port 5199
    check_existing_instance()

    print("=" * 60)
    print("  CertifyAI - Certificate Verification System")
    print("=" * 60)
    print(f"\n✓ Starting server on {URL}...")
    print("✓ Browser will open automatically...")
    print("\nPress Ctrl+C or use 'Stop Server' in browser to exit\n")
    
    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start server
    from app import app
    uvicorn.run(app, host='127.0.0.1', port=PORT, log_level='info')

if __name__ == '__main__':
    main()
