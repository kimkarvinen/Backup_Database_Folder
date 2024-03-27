import subprocess
import os
import shutil
import os
from pathlib import Path
from datetime import datetime
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"

# Close running applications
processes_to_close = ["posread.exe", "poswin.exe", "tsceressql.exe", "finedine.exe", "bacchussql.exe"]
for process in processes_to_close:
    subprocess.run(["taskkill", "/IM", process, "/F"], shell=True)

# Display message
def display_progress():
    print(COLOR_RED + "Please do not use the point-of-sale (POS) system during the backup process." + COLOR_RESET)
    print(COLOR_RED + "Backup process is in progress... Please Wait." + COLOR_RESET)
display_progress()

# Get current date in YYYYMMDD format
datestamp = datetime.now().strftime("%Y%m%d")
backup_count = 1
zipbackup_count = 1
source = "data"
destination = f"data_{datestamp}-{backup_count}"

# Check and increment backup count if destination directory exists
while os.path.exists(destination):
    backup_count += 1
    destination = f"data_{datestamp}-{backup_count}"
    
    

os.mkdir(destination)

# Get the path to the desktop directory
desktop_path = Path.home() / 'Desktop'

# Specify the name of the folder you want to create
backup_folder = 'POS_Backup'

# Create the folder on the desktop
folder_path = desktop_path / backup_folder
os.makedirs(folder_path, exist_ok=True)


# Copy files and subdirectories from source to destination
subprocess.run(["xcopy", "/E", "/I", "/Y", source, destination], shell=True,)
display_progress()

# Set zip destination : current folder
# zip_destination = f"data_store_name-{datestamp}-{zipbackup_count}.zip"
# Set zip destination : sample desktop or your own desired path
zip_destination = folder_path / f'data_store_name-{datestamp}-{zipbackup_count}.zip'

# Check and increment zipbackup_count if zip file already exists
while os.path.exists(zip_destination):
    zipbackup_count += 1
    zip_destination = folder_path / f'data_store_name-{datestamp}-{zipbackup_count}.zip'


# Zip the folder into another destination
powershell_command = rf"Compress-Archive -Path {destination} -DestinationPath {zip_destination}"
subprocess.run(["powershell", "-command", powershell_command], shell=True)


# Check if zip file creation was successful
if not os.path.exists(zip_destination):
    print(f"Error: Failed to create zip file {zip_destination}.")
    print("--Kim Karvinen")
    input("press any key to continue")
    exit()
    
print(COLOR_GREEN + f"Backup completed and zipped to {zip_destination}." + COLOR_RESET)
print(COLOR_GREEN + "The backup file is named based on your computer's date (YYYYMMDD)." + COLOR_RESET)
print(COLOR_GREEN + "You can upload the zip backup to your Google Drive" + COLOR_RESET)
print(COLOR_GREEN + "or copy the backup files to your flash drive." + COLOR_RESET)
print(COLOR_GREEN + "You may now resume using the point-of-sale (POS) system. Thank you for your patience." + COLOR_RESET) 
input(COLOR_GREEN + "press any key to continue" + COLOR_RESET)
