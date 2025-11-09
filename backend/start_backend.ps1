# Start VeriSyntra Backend Server
# This script starts the backend in a separate PowerShell window to prevent shutdown from subsequent commands
# Follows VeriSyntra coding standards for backend server management

Write-Host "[OK] Starting VeriSyntra backend in new window on http://localhost:8000" -ForegroundColor Green
Write-Host "[INFO] Backend will run in separate PowerShell window" -ForegroundColor Cyan

# Start backend in separate window (prevents shutdown from subsequent commands)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\backend; python main_prototype.py"

Write-Host "[OK] Backend server started" -ForegroundColor Green
Write-Host "[INFO] Verify server is running: (Invoke-WebRequest -Uri 'http://localhost:8000/docs' -UseBasicParsing).StatusCode" -ForegroundColor Yellow
