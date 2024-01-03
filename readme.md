# ATSMS - American Truck Simulator Management System

## Introduction

ATSMS is a server management tool designed for American Truck Simulator (ATS). This tool facilitates server configuration, management, and administration for ATS server instances.

## Configuration

The ATSMS configuration file `config.py` contains various settings to customize the tool. Make sure to adjust the following configurations before running the system:

### Webserver

- `PORT`: Port number for the webserver.
- `HOST`: Host address for the webserver.
- `SECRET_KEY`: Secret key for Flask sessions.
- `DEBUG`: Enable or disable Flask debug mode.

### Authentication

- `PASSWORD`: The administrative password for accessing ATSMS. **WARNING**: This password is stored in plain text and may pose a security risk. Avoid using passwords for critical purposes or reusing important passwords.

### ATS

- `USER_DATA_DIR`: Path to the ATS userdata directory.
- `DEFAULT_CONFIG`: Path to the default server.sii config file.
- `SERVER_EXE`: Path to the ATS server executable.

**Note**: Ensure the paths are correctly set according to your system setup.

## Running ATSMS

To start ATSMS, execute the `start_atsms.bat` file. This batch script handles the setup process:

```batch
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
