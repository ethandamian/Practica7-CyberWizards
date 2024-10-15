import platform
import os
import pwd
import grp
import psutil
from pathlib import Path
import crypt

logfile = "system_info.txt"

def write_to_file(content):
    with open(logfile, 'a') as file:
        file.write(content + "\n")

def get_system_info():
    write_to_file("=== System Information ===")
    write_to_file(f"Operating System: {platform.system()}")
    write_to_file(f"Version: {platform.version()}")
    write_to_file(f"Platform: {platform.platform()}")
    write_to_file(f"Architecture: {platform.architecture()}")
    write_to_file(f"Kernel: {platform.release()}")

def get_active_processes():
    write_to_file("\n=== Active Processes ===")
    for process in psutil.process_iter(['pid', 'name', 'username']):
        write_to_file(f"PID: {process.info['pid']}, Name: {process.info['name']}, User: {process.info['username']}")

def get_users_and_groups():
    write_to_file("\n=== Users and Groups ===")
    write_to_file("Users:")
    for user in pwd.getpwall():
        write_to_file(f"User: {user.pw_name}, UID: {user.pw_uid}, Home: {user.pw_dir}, Shell: {user.pw_shell}")
    write_to_file("\nGroups:")
    for group in grp.getgrall():
        write_to_file(f"Group: {group.gr_name}, GID: {group.gr_gid}, Members: {', '.join(group.gr_mem)}")

def get_password_hashes():
    write_to_file("\n=== Password Hashes (Requires root permissions) ===")
    try:
        with open('/etc/shadow', 'r') as shadow_file:
            for line in shadow_file:
                parts = line.split(':')
                user = parts[0]
                hash = parts[1]
                write_to_file(f"User: {user}, Hash: {hash}")
    except PermissionError:
        write_to_file("Permission denied. Run the script as root to read /etc/shadow.")

def get_files_in_home():
    write_to_file("\n=== Files in the User's Home Directory ===")
    home_path = Path.home()
    for file in home_path.rglob('*'):
        try:
            if file.is_file():
                file_type = "File"
            elif file.is_dir():
                file_type = "Directory"
            else:
                file_type = "Other"
            write_to_file(f"Type: {file_type}, Name: {file.name}, Size: {file.stat().st_size} bytes")
        except FileNotFoundError:
            write_to_file(f"Type: Unknown, Name: {file.name}, Error: File not found")

if __name__ == "__main__":
    # Clear the file before writing new content.
    with open(logfile, 'w') as file:
        file.write("System Information Report\n")
        file.write("="*30 + "\n")

    get_system_info()
    get_active_processes()
    get_users_and_groups()
    get_password_hashes()
    get_files_in_home()

    print(f"System information has been written to {logfile}.")
