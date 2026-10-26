@echo off
setlocal

set ROOT=%~dp0
cd /d %ROOT%

echo [1/2] Building spinal cord core with GCC...
if not exist build mkdir build
gcc -O2 -shared -o build\actuator_core.dll src\spinal_cord\actuator_core.c
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo [2/2] Launching orchestrator...
python main.py --offline
