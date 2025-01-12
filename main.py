"""
This program will sort files in a directory by their creation date and separate them by date.
Directories are skipped
"""
import os
from datetime import datetime
import shutil

directory = "C:/Users/justi/Downloads/test"
backup_directory = os.path.join(directory, "_BACKUP_")
log_file = os.path.join(directory, "log.txt")

def log_action(message):
    with open(log_file, "a") as log:
        log.write(f"{datetime.now()}: {message}\n")

def get_sort_key(file):
    file_path = os.path.join(directory, file)
    if len(file) >= 8 and file[:8].isdigit():
        return datetime.strptime(file[:8], "%Y%m%d")
    elif os.path.isdir(file_path):
        return datetime.min
    return datetime.fromtimestamp(os.path.getmtime(file_path))

def sort_files_by_date(directory):
    files = os.listdir(directory)
    sorted_files = sorted(files, key=get_sort_key)
    files_by_date = {}

    for file in sorted_files:
        if os.path.isdir(os.path.join(directory, file)) or file == "log.txt":
            continue  # Skip directories and the log file
        date_key = get_sort_key(file).date().strftime("%Y_%m_%d")
        files_by_date.setdefault(date_key, []).append(file)

    return files_by_date

def move_files(files_by_date, directory):
    if not any(files_by_date.values()):
        log_action("No files to move.")
        print("No files to move.")
        return

    # Create backup directory and copy files before sorting only if they don't exist in the destination
    os.makedirs(backup_directory, exist_ok=True)  # Ensure backup directory exists
    for date, files in files_by_date.items():
        date_directory = os.path.join(directory, date)
        os.makedirs(date_directory, exist_ok=True)

        for file in files:
            destination_path = os.path.join(date_directory, file)
            if os.path.exists(destination_path):
                log_action(f"Warning: File '{file}' already exists in '{date_directory}'. Skipping backup.")
                print(f"Warning: File '{file}' already exists in '{date_directory}'. Skipping backup.")
                continue
            shutil.copy2(os.path.join(directory, file), os.path.join(backup_directory, file))  # Backup the file
            log_action(f"Backed up file: {file}")

    total_files = sum(len(files) for files in files_by_date.values())
    log_action(f"Found {total_files} files")
    print(f"Found {total_files} files")
    print("Files sorted and separated by date:")
    
    for date, files in files_by_date.items():
        print(date)
        date_directory = os.path.join(directory, date)
        os.makedirs(date_directory, exist_ok=True)

        for file in files:
            destination_path = os.path.join(date_directory, file)
            if os.path.exists(destination_path):
                log_action(f"Warning: File '{file}' already exists in '{date_directory}'. Skipping move.")
                print(f"Warning: File '{file}' already exists in '{date_directory}'. Skipping move.")
                continue
            log_action(f"Moving file '{file}' to '{date_directory}'")
            print(f"  {file}")
            shutil.move(os.path.join(directory, file), destination_path)
        print()

files_by_date = sort_files_by_date(directory)
move_files(files_by_date, directory)