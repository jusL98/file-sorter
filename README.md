<a id="readme-top"></a>

# File Sorter

This program is a tool to automate organizing files into folders by date. The program first sorts files by the naming format YYYYMMDD, standard of smartphone camera file naming, otherwise by creation date if the file name does not follow that format. The tool enables the user to specify the source and target directories, whether to backup files, and the file types to include and exclude in the config.json file. Extensive logging and error handling is implemented.

<p align="left">
   <img width="600" alt="image" src="https://github.com/user-attachments/assets/bca85f09-f24d-4657-92fd-23e8d755b051"/>
</p>

<p align="left">
   <img width="600" alt="image" src="https://github.com/user-attachments/assets/1bf0f0f6-f66b-4bd1-9f1c-d392aa2adaaa"/>
</p>

## Description

File Sorter involves the user configuring the following settings in `config.json`:
- the source directory
- the target directories
- whether to backup files
- file types to include
- file types to exclude file

Then, the program can be run to result in a sorted file structure in the target directory, formatted YYYY_MM_DD. A log file will be created to track the file movements and any errors/skips. If backup is enabled, all unsorted files are copied to a backup folder within the target directory.

## Built With

- [Python 3.13](https://www.python.org/): Programming language for complete functionality

## Quick Start

### Prerequisites

- OS
- Python 3.13 or higher
- Terminal or CLI Access

### Installation

To install File Sorter, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/jusL98/file-sorter.git
   cd file-sorter
   ```

2. Ensure that you have python running on your system.

### Setup

3. Open `config.json`:

   - On Windows:

      ```bash
      notepad config.json
      ```

   - On macOS or Linux

      ```bash
      open config.json
      ```

7. Edit the configuration settings to satisfy your needs:

   - source_directory: Enter the path to the folder containing the files to be sorted.
   - target_directory: Enter the path to the folder where the sorted files will be placed.
   - backup_wanted: Enter 'true' or 'false' to enable or disable file backups.
   - file_types_to_include: Enter an array of file types to include in the sorting process. A blank array will include all file types not excluded below.
   - file_types_to_exclude: Enter an array of file types to exclude from the sorting process.

   ex. `config.json`
   ```bash
   {
   "source_directory": "C:/Users/justi/Downloads/source_dir_test",
   "target_directory": "C:/Users/justi/Downloads/source_dir_test/target_dir_test",
   "backup_wanted": true,
   "file_types_to_include": [],
   "file_types_to_exclude": [".mp4"]
   }
   ```

### Run

8. Run File Sorter:
   ```bash
   python main.py
   ```
9. Navigate to the target directory and view the sorted files in date folders formatted by YYYY_MM_DD along with the log file.

## Usage

1. Configure the settings in the config.json file.
2. Run the program.
3. Navigate to the target directory and view the sorted files in date folders formatted by YYYY_MM_DD.
4. Actions are logged in the log.txt file in the target directory.
5. If backup is enabled, the files (unsorted) were also copied to the backup directory within the target directory.

## Contributing

1. Fork & branch off main.
2. Make your changes.
3. PRs welcome!

## Project Structure

```
├── file-sorter/
│   ├── main.py                        # contains the main program code and logic
│   └── config.json                    # contains configuration settings
```

## Acknowledgements
This project was created for myself after recognizing the extensive time I spent manually sorting files into folders by date after downloading them from my phone.

## License
This project is licensed under the [MIT](LICENSE.txt) License. See LICENSE.txt for more information.

<br>

---

Thank you!

<p align="left">
  <a href="mailto:justin.matthew.lee.18@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
  </a>
  <a href="https://www.linkedin.com/in/justin-matthew-lee/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>
    <a href="https://github.com/jusl98">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
</p>

<p align="right">(<a href="#readme-top">BACK TO TOP</a>)</p>
