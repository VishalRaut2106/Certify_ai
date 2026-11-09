
import sys
sys.path.insert(0, r"V:\Desktop\Certificate\certificate-verification-system\backend")
import uvicorn
from app import app
uvicorn.run(app, host="127.0.0.1", port=5199, log_level="error")
