@echo off

set VENV_FOLDER=venv

REM Check if venv folder exists, create it if not
if not exist %VENV_FOLDER% (
    python -m venv %VENV_FOLDER%
)

REM Activate the virtual environment
call %VENV_FOLDER%\Scripts\activate

REM Install requirements using pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found
    exit /b 1
)

REM Run your Python script
python run.py
