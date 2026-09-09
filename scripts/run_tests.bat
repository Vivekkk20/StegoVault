@echo off
echo ===================================================
echo   StegoVault - Test and Verification Suite
echo ===================================================
echo.
echo [1/3] Running Backend Pytest Suite...
cd /d %~dp0..\backend
call .venv\Scripts\pytest -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Backend tests failed!
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Verifying Test Dataset Generation...
call .venv\Scripts\python %~dp0generate_test_data.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Dataset generation failed!
    exit /b %ERRORLEVEL%
)

echo.
echo [3/3] Verifying Frontend TypeScript and Build...
cd /d %~dp0..\frontend
call npm.cmd run build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Frontend build failed!
    exit /b %ERRORLEVEL%
)

echo.
echo ===================================================
echo   All StegoVault Verification Tests Passed!
echo ===================================================
