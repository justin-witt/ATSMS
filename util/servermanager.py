"""
File: servermanager.py
Author: Justin Wittenmeier
Description: Main file for server management tool.

Last Modified: January 7, 2024
"""

import os, random, string, subprocess, shutil

# Classes
class Server:
    def __init__(self, id : str, is_running : bool) -> None:
        self.ID : str = id
        self.name : str = get_server_name(get_cfg(id)) 
        self.running : bool = is_running
        self.player_count : str = get_player_count(id)

# Global variables
__server_exe : str = None # Path to server executable
__data_path : str = None # Path to server userdata directory
__default_cfg : str = None # Path to default server configuration
__DB_FOLDER : str = "atsms" # Folder name for server data
__servers : dict = {} # Container for running servers. # Removed test server from this in v0.1.1
__LOG_FOLDER : str = f"server.log.{__DB_FOLDER}" # Folder name for server logs (Added in v0.1.1)

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
    Initializes the manager with the provided executable path, data path, and default configuration path.

    Parameters:
        exe_path (str): The path to the server executable.
        data_path (str): The path to the data folder.
        default_cfg_path (str): The path to the default configuration file.

    Returns:
        None

    Raises:
        None

    Notes:
        - This function should only be called once to initialize the manager.
        - If the manager has already been initialized, this function does nothing.
        - The executable path, data path, and default configuration path must be valid paths on the system.
    """
    global __data_path, __server_exe, __default_cfg

    if __server_exe or __data_path or __default_cfg:
        print("Server manager already initialized.")
        return
    
    __set_vars(exe_path, data_path, default_cfg_path)
    __folder_setup()

    for folder in os.listdir(__db_path()):
        __atsm_launch_log(folder)
    
    print("Initialized manager.")

def get_servers() -> list:
    """
    Get a list of servers.
    Returns:
        list: A list of server ids.
    """

    servers : list = []
    folders = os.listdir(__db_path())

    for folder in folders:
        
        logs = get_logs(folder, 1)
        logs = logs if logs else ["none"]

        running = folder in get_running_servers()

        if "[sys] Process manager shutdown." in logs[0] and running:
            stop_server(folder)
            __atsm_shutdown_error(folder)
            running = False

        if running:
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
        #this fixes the issue of it adding whitespace between each line when saving (fixed in v0.1.2)
        f.write("\n".join(data.splitlines()))
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

#Added in v0.1.1
def get_logs(id : str, limit : int = 50) -> list[str]:
    """
    Returns the last `limit` lines of the server.txt file for the given `id`. If limit is 0, all lines are returned.

    Parameters:
        id (str): The ID of the file.
        limit (int): The number of lines to return. Defaults to 50.

    Returns:
        str: The last `limit` lines of the server.txt file.
    """
    target = os.path.join(__data_path, __LOG_FOLDER, id, "server.txt")
    try:
        with open(target, 'r') as f:
            lines = f.read().splitlines()
            if limit:
                return lines[-limit:]
            else:
                return lines
    except FileNotFoundError:
        return []

def get_running_servers() -> list:
    """
    Returns a list of the running servers.

    :return: A list of the server keys.
    :rtype: list
    """
    return list(__servers.keys())

#Added in v0.1.1
def get_player_count(id : str) -> str:
    """
    Retrieves the player count for a given ID.

    Parameters:
        id (str): The ID of the player.

    Returns:
        str: The player count as a string.
    """
    data = get_logs(id, 25)[::-1]
    for line in data:
        if "Players:" in line:
            return line[-1]
    else : return "0"

#added in v0.1.1
def __atsm_shutdown_error(id : str) -> None:
    """
    Write a critical error message to the server log file.

    Args:
        id (str): The identifier of the server.

    Returns:
        None
    """
    with open(os.path.join(__data_path, __LOG_FOLDER, id, "server.txt"), 'a') as f:
        f.write("[atsm] ATSMS shutdown CRITICAL ERROR - PROCESS SHUTDOWN\n")

#added in v0.1.1
def __atsm_launch_log(id : str) -> None:
    """
    Writes the launch log for the ATSM server.

    Args:
        id (str): The ID of the server.

    Returns:
        None
    """
    try:
        with open(os.path.join(__data_path, __LOG_FOLDER, id, "server.txt"), 'a') as f:
            f.write("[atsm] ATSMS launched\n")
    except FileNotFoundError:
        pass

#added in v0.1.1
def shutdown():
    """
    Shutdown all running servers by calling the `stop_server` function for each server ID returned by the `get_running_servers` function.
    """
    for id in get_running_servers():
        stop_server(id)

def get_server_name(data : str) -> str :
    """
    Gets the server name from the `data` string.

    Args:
        data (str): The input data.
    
    Returns:
        str: The extracted server name.
    """
    data = data.split('lobby_name:')
    data = data[1].split('\n')[0].strip()
    data = data.replace('"', '')
    return data