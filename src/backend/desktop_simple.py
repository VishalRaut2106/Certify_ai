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

def create_desktop_shortcut():
    """Create a desktop shortcut if it doesn't exist and we are running as an exe"""
    if not getattr(sys, 'frozen', False):
        return  # Only create shortcut for the built .exe
        
    import subprocess
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    shortcut_path = os.path.join(desktop, 'CertifyAI.lnk')
    
    if not os.path.exists(shortcut_path):
        exe_path = sys.executable
        # Use PowerShell to create the shortcut using Windows COM objects (no pip packages needed)
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
