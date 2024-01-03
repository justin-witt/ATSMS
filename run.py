"""
File: run.py
Author: Justin Wittenmeier
Description: Main file for server management tool.

Version: v0.1.0-alpha-2024.01.02
Last Modified: January 1, 2024

"""

import config, routes
from auth import app

app.register_blueprint(routes.views_bp)

def main():
    app.run(debug=config.DEBUG,host=config.HOST,port=config.PORT)

if __name__ == "__main__":
    main()