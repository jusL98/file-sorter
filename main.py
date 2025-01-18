"""
This program will sort files in a directory by their creation date and separate them by date.
Directories are skipped
"""
# Imports
import os
from datetime import datetime
import shutil

# DIRECTORY, BACKUP FOLDER NAME, LOG FILE NAME, BACKUP OPTION
directory = "C:/Users/justi/Downloads/test"
log_file = os.path.join(directory, "log.txt")
backup_wanted = True
file_types_to_include = []  # Add file extensions to exclude (ex. ['.jpg', '.pdf']), empty list means all file types not excluded below are included.
file_types_to_exclude = [".mp4", ".exe"]  # Add file extensions to exclude (ex. ['.exe', '.tmp']), empty list means no exclusions.
# --------------------------------------------

# Handles logging and printing messages.
def log_message(message, level="info"):
    levels = {
        "decorating": "",
        "info": "",
        "moving": "",
        "warning": "Warning: ",
        "error": "Error: "
    }
    prefix = levels.get(level, "")
    full_message = f"{prefix}{message}"

    if level == "info":
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()}: {full_message}\n")
    if level == "moving" or level == "warning" or level == "error":
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()}:  --> {full_message}\n")
    elif level == "decorating":
        with open(log_file, "a") as log:
            log.write(full_message)
    print(full_message)

# Gets the sort method for each file either based on the file name of YYYYMMDD (first 8 digits), otherwise if not named like that, based on creation date.
def get_sort_key(file):
    file_path = os.path.join(directory, file) 

    # Sorts by file name
    if len(file) >= 8 and file[:8].isdigit():
        return datetime.strptime(file[:8], "%Y%m%d")
    
    # Sorts by creation date
    else:
        return datetime.fromtimestamp(os.path.getmtime(file_path))

# Sorts and orders files and stores it in a dictionary. If the file is a directory or the log file, it will skip it.
def sort_files_by_date(directory):
    files = os.listdir(directory)
    sorted_files = sorted(files, key=get_sort_key)
    grouped_files = {}

    for file in sorted_files:
        file_path = os.path.join(directory, file)
        
        # Skip directories and the log file
        if os.path.isdir(file_path) or file_path == log_file:
            continue

        date_key = get_sort_key(file).date().strftime("%Y_%m_%d")
        grouped_files.setdefault(date_key, []).append(file) # Groups files by the same date key together, creates a new key under the date key if it doesn't exist.
    return grouped_files

# Moves files to their respective date folders and creates a backup of the files before moving them.
def move_files(grouped_files, directory):
    total_files_found = sum(len(files) for files in grouped_files.values())
    total_files_moved = 0

    log_message(f"TOTAL FILES FOUND: {total_files_found}\n", level="decorating")

    # Checks if there are no files to move.
    if not total_files_found:
        log_message("No files to move. Exiting.")
        log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating")
        return total_files_found, total_files_moved

    # Creates a backup directory if backup is wanted.
    if backup_wanted:
        backup_directory = os.path.join(directory, "_BACKUP_")
        os.makedirs(backup_directory, exist_ok=True)

    for date, files in grouped_files.items():
        # Creates a directory for each date.     
        date_directory = os.path.join(directory, date)
        if not os.path.exists(date_directory):
            os.makedirs(date_directory, exist_ok=True)
            log_message(f"New directory created: {date}")
        else:
            log_message(f"Using existing directory: {date}")

        for file in files:
            source_path = os.path.join(directory, file)
            destination_path = os.path.join(date_directory, file)

            # Checks and handles if the file already exists in the destination directory.
            if os.path.exists(destination_path):
                log_message(f"File '{file}' already exists in '{date_directory.replace(os.sep, '/')}'. Skipping move. {'Backup not created.' if backup_wanted else ''}", level="warning")
                continue
            
            # Check file extension against whitelist and blacklist.
            file_extension = os.path.splitext(file)[1].lower()
            if file_types_to_include and file_extension not in file_types_to_include:
                log_message(f"File '{file}' excluded ({file_extension} not in include list). Skipping move. {'Backup not created.' if backup_wanted else ''}", level="warning")
                continue
            if file_extension in file_types_to_exclude:
                log_message(f"File '{file}' excluded ({file_extension} in exclude list). Skipping move. {'Backup not created.' if backup_wanted else ''}", level="warning")
                continue

            # Backups the file if backup is wanted and overwrites the previous backup file if it already exists.
            if backup_wanted:
                shutil.copy2(source_path, os.path.join(backup_directory, file))

            # Moves the file to the date directory.
            log_message(f"Moving file '{file}' to '{date_directory.replace(os.sep, '/')}'. {'Backup created.' if backup_wanted else ''}", level="moving")
            shutil.move(source_path, destination_path)
            total_files_moved += 1

    log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating")
    return total_files_found, total_files_moved

def main():
    log_message("**************************************************\n", level="decorating")
    log_message(f"New Log Entry - {datetime.now()}\n", level="decorating")
    log_message("**************************************************\n", level="decorating")

    log_message("Settings:\n", level="decorating")
    log_message(f"  - Target Directory: {directory}\n", level="decorating")
    log_message(f"  - Backup: {'enabled' if backup_wanted else 'disabled'}\n", level="decorating")
    log_message(f"  - File Types To Include: {', '.join(file_types_to_include) if file_types_to_include else 'All'}\n", level="decorating")
    log_message(f"  - File Types To Exclude: {', '.join(file_types_to_exclude) if file_types_to_exclude else 'None'}\n", level="decorating")

    log_message("--------------------------------------------------\n", level="decorating")

    log_message("\n", level="decorating")

    grouped_files = sort_files_by_date(directory)
    move_files(grouped_files, directory)

    log_message("\n==================================================\n", level="decorating")

    log_message("\n\n\n\n", level="decorating")

if __name__ == "__main__":
    main()