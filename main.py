"""
This program will take a source directory and sort files within the directory by their creation date.
New date directories are created if they do not already exist.
Files are moved to their respective date directories.

Settings can be modified including:
- Source directory
- Target directory
- Backup: Enabled or Disabled
- File types to include
- File types to exclude
"""

# Imports
import os
import json
from datetime import datetime
import shutil

# Load settings from config.json.
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

config = load_config()

source_directory = config['source_directory']
target_directory = config['target_directory']
backup_wanted = config['backup_wanted']
file_types_to_include = config['file_types_to_include']
file_types_to_exclude = config['file_types_to_exclude']


log_file = os.path.join(target_directory, "log.txt")
backup_directory = os.path.join(target_directory, "_BACKUP_")
# --------------------------------------------

# Handles logging and printing messages.
def log_message(message, level="info"):
    levels = {
        "info": "",
        "moving": "MOVING: ",
        "warning": "WARNING: ",
        "error": "ERROR: ",
        "decorating": ""
    }
    prefix = levels.get(level, "")
    base_message = f"{prefix}{message}"
    
    if level == "info":
        final_message = f"{datetime.now()}: {base_message}\n"
    elif level == "moving":
        final_message = f"{datetime.now()}:  --> {base_message} {'Backup created.' if backup_wanted else ''}\n"
    elif level == "warning":
        final_message = f"{datetime.now()}:  --> {base_message} Skipping move. {'Backup not created.' if backup_wanted else ''}\n"
    elif level == "error":
        final_message = f"{datetime.now()}: {base_message} Exiting.\n"
    elif level == "decorating":
        final_message = base_message

    with open(log_file, "a") as log:
        log.write(final_message)

# Gets the sort method for each file either based on the file name of YYYYMMDD (first 8 digits), otherwise if not named like that, based on creation date.
def get_sort_key(file):
    file_path = os.path.join(source_directory, file) 

    # Sorts by file name
    if len(file) >= 8 and file[:8].isdigit():
        return datetime.strptime(file[:8], "%Y%m%d")
    
    # Sorts by creation date
    else:
        return datetime.fromtimestamp(os.path.getmtime(file_path))

# Sorts and orders files and stores it in a dictionary. If the file is a directory or the log file, it will skip it.
def sort_files_by_date(source_directory):
    files = os.listdir(source_directory)
    sorted_files = sorted(files, key=get_sort_key)
    grouped_files = {}

    for file in sorted_files:
        file_path = os.path.join(source_directory, file)
        
        # Skip directories and the log file.
        if os.path.isdir(file_path) or file_path == log_file: #or file_path == os.path.join(source_directory, "log.txt"): <-- This is to also skip a log file if in the source directory.
            continue

        date_key = get_sort_key(file).date().strftime("%Y_%m_%d")
        grouped_files.setdefault(date_key, []).append(file) # Groups files by the same date key together, creates a new key under the date key if it doesn't exist.
    return grouped_files

# Moves files to their respective date folders and creates a backup of the files before moving them.
def move_files(grouped_files, source_directory):
    total_files_found = sum(len(files) for files in grouped_files.values())
    total_files_moved = 0

    log_message(f"TOTAL FILES FOUND: {total_files_found}\n", level="decorating")

    # EXIT 1 - Check for conflicts between whitelist and blacklist
    if set(file_types_to_include) & set(file_types_to_exclude):
        log_message("Conflict detected between whitelist and blacklist.", level="error")
        log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating")
        print("ERROR: Conflict detected between whitelist and blacklist.")
        return total_files_found, total_files_moved

    # EXIT 2 - Checks if there are no files to move.
    if not total_files_found:
        log_message("No files to move.", level="error")
        log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating")
        print("ERROR: No files to move.")
        return total_files_found, total_files_moved

    # Creates a backup directory if backup is wanted.
    if backup_wanted:
        os.makedirs(backup_directory, exist_ok=True)

    for date, files in grouped_files.items():
        # Creates a directory for each date.     
        date_directory = os.path.join(target_directory, date)
        if not os.path.exists(date_directory):
            os.makedirs(date_directory, exist_ok=True)
            log_message(f"New directory created: {date}")
        else:
            log_message(f"Using existing directory: {date}")

        for file in files:
            source_path = os.path.join(source_directory, file)
            destination_path = os.path.join(date_directory, file)

            # FILE SKIP 1 - Checks and handles if the file already exists in the destination directory.
            if os.path.exists(destination_path):
                log_message(f"File '{file}' already exists in '{date_directory.replace(os.sep, '/')}'.", level="warning")
                continue
            
            # FILE SKIP 2 - Check file extension against whitelist and blacklist.
            file_extension = os.path.splitext(file)[1].lower()
            if file_types_to_include and file_extension not in file_types_to_include:
                log_message(f"File '{file}' excluded ({file_extension} not in include list).", level="warning")
                continue
            if file_extension in file_types_to_exclude:
                log_message(f"File '{file}' excluded ({file_extension} in exclude list).", level="warning")
                continue

            # Backups the file if backup is wanted and overwrites the previous backup file if it already exists.
            if backup_wanted:
                shutil.copy2(source_path, os.path.join(backup_directory, file))

            # Moves the file to the date directory.
            log_message(f"File '{file}' to '{date_directory.replace(os.sep, '/')}'.", level="moving")
            shutil.move(source_path, destination_path)
            total_files_moved += 1

    log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating")
    print("Completed.")
    print(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}")
    return total_files_found, total_files_moved

def main():
    # Ensure the source directory exists
    if not os.path.exists(source_directory):
        print('ERROR: Source directory does not exist.')
        return

    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        print('ERROR: Target directory does not exist.')
        return
    
    log_message("**************************************************\n", level="decorating")
    log_message(f"New Log Entry - {datetime.now()}\n", level="decorating")
    log_message("**************************************************\n", level="decorating")

    log_message("Settings:\n", level="decorating")
    log_message(f"  - Source Directory: {source_directory}\n", level="decorating")
    log_message(f"  - Target Directory: {target_directory}\n", level="decorating")
    log_message(f"  - Backup: {'Enabled' if backup_wanted else 'Disabled'}\n", level="decorating")
    log_message(f"  - File Types To Include: {', '.join(file_types_to_include) if file_types_to_include else 'All'}\n", level="decorating")
    log_message(f"  - File Types To Exclude: {', '.join(file_types_to_exclude) if file_types_to_exclude else 'None'}\n", level="decorating")

    log_message("--------------------------------------------------\n", level="decorating")

    log_message("\n", level="decorating")

    grouped_files = sort_files_by_date(source_directory)
    move_files(grouped_files, source_directory)

    log_message("\n==================================================\n", level="decorating")

    log_message("\n\n\n\n", level="decorating")

if __name__ == "__main__":
    main()