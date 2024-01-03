# Configurations for server management tool.

# Webserver
PORT = 5500 # Port number
HOST = "0.0.0.0" # 0.0.0.0 is the default.
SECRET_KEY = "" # This will be generated if left empty.
DEBUG = False # Sets flask to debug mode.

# Authentication
# SECURITY WARNING: This password is stored in plain text and is not secure.
# Avoid using passwords for critical purposes or reusing important passwords.
PASSWORD = "admin.password"

# ATS
# NOTE: You need to update USER to the appropriate username for your system if you want to use these paths.
USER_DATA_DIR = r"C:\Users\USER\Documents\American Truck Simulator" # Path  to ATS userdata directory (Leave the 'r' at the beginning unchanged)
DEFAULT_CONFIG = r"C:\Users\USER\Documents\American Truck Simulator\server_config.sii" # Path to default server.sii config file to be copied to new servers (Leave the 'r' at the beginning unchanged)
SERVER_EXE = r"path/to/server.exe" # Path to ATS server executable (Leave the 'r' at the beginning unchanged)