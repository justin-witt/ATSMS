"""
File: run.py
Author: Justin Wittenmeier
Description: Main file for server management tool.

Version: v0.1.1
Last Modified: January 7, 2024

"""

import atexit
import config, routes
from util import servermanager
from auth import app

#add shutdown function in v0.1.1
atexit.register(servermanager.shutdown)

#initalize servermanager    
servermanager.init_manager(exe_path=config.SERVER_EXE, data_path=config.USER_DATA_DIR, default_cfg_path=config.DEFAULT_CONFIG)

app.register_blueprint(routes.views_bp)

def main():
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

if __name__ == "__main__":
    main()