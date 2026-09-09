@echo off
echo ===================================================
echo   StegoVault - Local Development Environment
echo ===================================================
echo Starting Backend on http://127.0.0.1:8000 ...
start "StegoVault Backend" cmd /k "cd /d %~dp0..\backend && .venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo Starting Frontend on http://127.0.0.1:5173 ...
start "StegoVault Frontend" cmd /k "cd /d %~dp0..\frontend && npm run dev"

echo.
echo StegoVault services launched in separate windows!
echo - Backend API: http://127.0.0.1:8000 (API Docs: http://127.0.0.1:8000/docs)
echo - Frontend Dashboard: http://127.0.0.1:5173
echo.
pause
