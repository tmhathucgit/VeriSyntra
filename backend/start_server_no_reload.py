"""
Simple server starter without reload mode
Avoids multiprocessing issues with Windows
"""
import uvicorn
from main_prototype import app

if __name__ == "__main__":
    print("[OK] Starting VeriSyntra server without reload...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
