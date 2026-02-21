@echo off
REM ============================================================
REM STRUCTIFY STARTUP SCRIPT
REM ============================================================
REM This script starts both the backend and frontend servers
REM ============================================================

setlocal enabledelayexpand

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║         STRUCTIFY PROTOTYPE STARTUP                     ║
echo ║      Backend + Frontend + Browser                      ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if we're in the right directory
if not exist "Backend" (
    echo ERROR: Run this from the Structify root directory
    echo Current directory: %cd%
    pause
    exit /b 1
)

echo [1/2] Starting Backend Server...
echo      Location: Backend/
echo      URL: http://127.0.0.1:8001
echo      Keep this window open while using the app
echo.

start cmd /k "cd Backend && python -m uvicorn main:app --host 127.0.0.1 --port 8001"

timeout /t 3 /nobreak

echo [2/2] Starting Frontend Server...
echo      Location: Frontend/
echo      URL: http://localhost:5500
echo      Keep this window open while using the app
echo.

start cmd /k "cd Frontend && python -m http.server 5500"

timeout /t 2 /nobreak

echo.
echo ✅ Both servers are starting...
echo.
echo 📝 Next Steps:
echo    1. Wait for both windows to show "Running" messages
echo    2. Your browser should open automatically
echo    3. If not, go to: http://localhost:5500/chat.html
echo.
echo 🛑 To stop:
echo    • Close both command windows
echo.
echo 💡 Troubleshooting:
echo    • Port 8001 or 5500 already in use?
echo      Check: netstat -ano | findstr "8001"
echo    • Backend connection failed?
echo      Make sure Frontend/config.js has BACKEND_URL: 'http://127.0.0.1:8001'
echo.

REM Try to open browser
powershell -Command "Start-Process 'http://localhost:5500/chat.html'" 2>nul

echo Waiting for servers...
timeout /t 5 /nobreak

echo.
echo ✨ Structify is ready!
echo    Open http://localhost:5500/chat.html in your browser
echo.
