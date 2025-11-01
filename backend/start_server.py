"""
Start VeriSyntra Backend Server
Simple startup script with error handling
"""

import sys
import os

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

try:
    print("[OK] Importing FastAPI application...")
    from main_prototype import app
    
    print("[OK] Starting Uvicorn server...")
    import uvicorn
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

except Exception as e:
    print(f"[ERROR] Failed to start server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
