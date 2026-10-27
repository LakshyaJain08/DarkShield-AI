@echo off
title DarkShield AI - One-Click Launcher
echo ========================================================
echo   Starting DarkShield AI Full-Stack Platform...
echo ========================================================
echo.

echo [1/3] Launching FastAPI Backend on http://127.0.0.1:8000 ...
start "DarkShield Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo [2/3] Launching React/Vite Frontend on http://localhost:5173 ...
start "DarkShield Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo [3/3] Opening Browser...
start http://localhost:5173

echo.
echo ========================================================
echo   DarkShield AI is running!
echo   - Web UI:  http://localhost:5173
echo   - Backend: http://127.0.0.1:8000
echo   - API Docs: http://127.0.0.1:8000/docs
echo ========================================================
pause
