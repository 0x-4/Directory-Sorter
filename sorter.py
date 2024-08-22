import os
import shutil
import time

def organize_files(directory, include_old_files):
    # these are all the defined file types that will get sorted
    file_types = {
        'Images': ['jpg', 'jpeg', 'png', 'gif'],
        'Documents': ['pdf', 'docx', 'txt', 'xlsx'],
        'Music': ['mp3', 'wav'],
        'Videos': ['mp4', 'avi', 'mov'],
        'Archives': ['zip', 'tar', 'gz', 'rar', '7zip']
    }
    
    # This will create the sorted folders in the set cleaned directory
    for folder in file_types:
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    # if selected yes, this will create an "old files" folder for things that havent been touched in over 30 days
    if include_old_files:
        old_files_folder = os.path.join(directory, 'Old_Files')
        if not os.path.exists(old_files_folder):
            os.makedirs(old_files_folder)
    
    # Gets the current time to check for old files
    current_time = time.time()
    thirty_days_seconds = 30 * 86400  # 30 days in seconds

    # Move files to appropriate folders
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # Check file modification time of files
            file_mod_time = os.path.getmtime(file_path)
            if include_old_files and (current_time - file_mod_time) > thirty_days_seconds:
                shutil.move(file_path, os.path.join(old_files_folder, filename))
                continue  # if the files old it skips over it
            
            ext = filename.split('.')[-1].lower()
            moved = False
            for folder, extensions in file_types.items():
                if ext in extensions:
                    shutil.move(file_path, os.path.join(directory, folder, filename))
                    moved = True
                    break
            if not moved:
                # moves files with file types that have not been defined into "others"
                others_folder = os.path.join(directory, 'Others')
                if not os.path.exists(others_folder):
                    os.makedirs(others_folder)
                shutil.move(file_path, os.path.join(others_folder, filename))

if __name__ == "__main__":
    directory = input("Enter the directory path to organize: ")
    include_old_files = input("create folder for files not modified in over 30 days? (yes/no): ").strip().lower()
    include_old_files = include_old_files == 'yes'
    organize_files(directory, include_old_files)
    print("Files have been organized.")
