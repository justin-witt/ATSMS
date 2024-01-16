"""
File: run.py
Author: Justin Wittenmeier
Description: Main file for server management tool.

Version: v0.1.3
Last Modified: January 16, 2024

"""

import atexit
import config, routes
from util import servermanager
from auth import app

#add shutdown function in v0.1.1
atexit.register(servermanager.shutdown)

#initalize servermanager
#the start_servers parameter was causing a problem when running in debug so if debug is true it will not start the servers automatically no matter what it's set too. 
servermanager.init_manager(exe_path=config.SERVER_EXE, data_path=config.USER_DATA_DIR, default_cfg_path=config.DEFAULT_CONFIG, start_servers=config.START_SERVERS if not config.DEBUG else False)

app.register_blueprint(routes.views_bp)

def main():
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

if __name__ == "__main__":
    main()