"""
File: servermanager.py
Author: Justin Wittenmeier
Description: Main file for server management tool.

Last Modified: January 1, 2024
"""

import os, random, string, subprocess, shutil

# Classes
class Server:
    def __init__(self, id : str, is_running : bool) -> None:
        self.ID : str = id
        self.running : bool = is_running

# Global variables
__server_exe : str = None # Path to server executable
__data_path : str = None # Path to server userdata directory
__DB_FOLDER : str = "atsms" # Folder name for server data
__default_cfg : str = None # Path to default server configuration
__servers : dict = { "test": "tested"} # Container for running servers.

# Functions
def __db_path() -> str:
    return os.path.join(__data_path, __DB_FOLDER)

def __set_vars(exe_path : str, data_path : str, default_cfg_path : str) -> None:
    global __data_path, __server_exe, __default_cfg
    __data_path = data_path
    __server_exe = exe_path
    __default_cfg = default_cfg_path

def __folder_setup() -> None:
    if not os.path.exists(__db_path()):
        os.mkdir(__db_path())
        print("Created folder: " + __db_path())
    else:
        print("Folder already exists: " + __db_path())

def init_manager(exe_path : str, data_path : str, default_cfg_path : str) -> None:
    """
    Initializes the manager with the provided executable path and data path.

    Parameters:
        exe_path (str): The path to the server executable.
        data_path (str): The path to the ats/ets user data folder.

    Returns:
        None
    """
    global __data_path, __server_exe, __default_cfg
    if __server_exe or __data_path or __default_cfg:
        print("Server manager already initialized.")
        return
    __set_vars(exe_path, data_path, default_cfg_path)
    __folder_setup()
    print("Initialized manager.")

def get_servers() -> list:
    """
    Get a list of servers.
    Returns:
        list: A list of server ids.
    """
    servers = []
    folders = os.listdir(__db_path())
    for folder in folders:
        if folder in __servers.keys():
            servers.append(Server(folder, True))
        else:
            servers.append(Server(folder, False))
    return servers

def __generate_server_id(length: int = 8) -> str:
    """
    Generates a random server ID of a specified length.

    Parameters:
        length (int): The length of the server ID. Defaults to 8.

    Returns:
        str: The randomly generated server ID.
    """
    characters = string.ascii_lowercase + string.digits  # Using lowercase letters and digits
    return ''.join(random.choice(characters) for _ in range(length))

def __copy_cfg(path : str) -> None:
    print("Copying cfg...")
    with open(__default_cfg, 'r') as src, open(path, 'w') as dest:
        dest.write(src.read())
    print("Copied cfg.")

def create_server() -> string:
    """
    Create a server and return its ID.
    
    Returns:
        string: The ID of the created server.
    """
    id = __generate_server_id()
    destination = os.path.join(__db_path(), id)
    print("Creating server: " + id)
    os.mkdir(destination)
    print("Created folder: " + id)
    __copy_cfg(os.path.join(destination, "server.sii"))
    print("Created server: " + id)
    return id

def delete_server(id : str) -> None:
    """
    Deletes a server with the given ID.

    Parameters:
        id (str): The ID of the server to be deleted.

    Returns:
        None
    """
    print("Deleting server: " + id)
    target = os.path.join(__db_path(), id)
    shutil.rmtree(target)
    print("Deleted server: " + id)

def edit_server(id : str, data : str) -> None:
    """
    Edit the server file with the given ID by replacing its content with the provided data.

    Parameters:
        id (str): The ID of the server file to be edited.
        data (str): The new content to be written to the server file.

    Returns:
        None
    """
    target = os.path.join(__db_path(), id, "server.sii")
    with open (target, 'w') as f:
        f.write(data)
    print("Edited server: " + id)

def start_server(id : str)  -> None:
    """
    Starts a server with the given ID.

    Parameters:
        id (str): The ID of the server.

    Returns:
        None
    """
    if id not in __servers:
        flags = ['-nosingle', '-server_cfg']
        config = __DB_FOLDER + "/" + id + "/server.sii"
        serverargs = flags + [config]
        server = subprocess.Popen([__server_exe] + serverargs)
        __servers[id] = server
        print("Started server: " + id)
    else:
        print("Server " + id + " is already running.")

def stop_server(id : str) -> None:
    """
    Stops a server with the given ID.

    Args:
        id (str): The ID of the server to stop.

    Returns:
        None
    """
    server = __servers.pop(id)
    server.terminate()
    server.kill()
    print("Stopped server: " + id)

def reset_cfg(id : str) -> None:
    """
    Resets the configuration file of a server with the given ID.

    Args:
        id (str): The ID of the server whose configuration file is to be reset.

    Returns:
        None
    """
    target = os.path.join(__db_path(), id, "server.sii")
    __copy_cfg(target)
    print("Reset server: " + id)

def get_cfg(id : str) -> str:
    """
    Returns the content of the server.sii file for the given `id`.

    Parameters:
        id (str): The ID of the file.

    Returns:
        str: The content of the server.sii file.
    """
    target = os.path.join(__db_path(), id, "server.sii")
    with open(target, 'r') as f:
        return f.read()

def get_running_servers() -> list:
    return list(__servers.keys())