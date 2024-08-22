import os
import shutil
import time

def organize_files(directory, include_old_files, old_files_days):
    # Define file types and their corresponding folders
    file_types = {
        'Images': ['jpg', 'jpeg', 'png', 'gif', 'svg', 'eps', 'ai', 'raw', 'nef', 'cr2', 'dng'],
        'Documents': ['pdf', 'docx', 'txt', 'xlsx', 'ppt', 'pptx', 'csv', 'ods', 'epub', 'mobi', 'azw', 'md'],
        'Music': ['mp3', 'wav', 'flac', 'alac', 'aac', 'ogg'],
        'Videos': ['mp4', 'avi', 'mov', 'webm', 'mkv', 'flv', 'ts'],
        'Archives': ['zip', 'tar', 'gz', 'rar', '7zip', 'bz2', 'lz', 'lzma', 'iso', 'dmg'],
        'Code': ['py', 'js', 'html', 'css', 'sh', 'bat', 'rb'],
        'System': ['conf', 'ini', 'json', 'exe', 'app', 'bin'],
        'Fonts': ['ttf', 'otf'],
        'Logs': ['log'],
        'Others': [] 
    }
    
    # Create folders if they don't exist
    for folder in file_types:
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    # Create 'Old_Files' folder if required
    if include_old_files:
        old_files_folder = os.path.join(directory, 'Old_Files')
        if not os.path.exists(old_files_folder):
            os.makedirs(old_files_folder)
    
    # Get the current time to check for old files
    current_time = time.time()
    old_files_seconds = old_files_days * 86400  # Convert days to seconds

    # Move files to appropriate folders
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            try:
                # Check file modification time
                file_mod_time = os.path.getmtime(file_path)
                if include_old_files and (current_time - file_mod_time) > old_files_seconds:
                    shutil.move(file_path, os.path.join(old_files_folder, filename))
                    continue
            
                ext = filename.split('.')[-1].lower()
                moved = False
                for folder, extensions in file_types.items():
                    if ext in extensions:
                        shutil.move(file_path, os.path.join(directory, folder, filename))
                        moved = True
                        break
                
                if not moved:
                    # Move files with unrecognized extensions to 'Others'
                    others_folder = os.path.join(directory, 'Others')
                    if not os.path.exists(others_folder):
                        os.makedirs(others_folder)
                    shutil.move(file_path, os.path.join(others_folder, filename))

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    while True:
        directory = input("Enter the directory path to organize: ").strip()
        if os.path.isdir(directory):
            break
        print("Invalid directory path. Please check and try again.")
    
    while True:
        try:
            old_files_days = int(input("Enter the number of days to consider a file as old: ").strip())
            if old_files_days < 0:
                print("Number of days must be a positive integer.")
            else:
                include_old_files = input("Create folder for files not modified in over X days? (yes/no): ").strip().lower()
                include_old_files = include_old_files == 'yes'
                organize_files(directory, include_old_files, old_files_days)
                print("Files have been organized.")
                break
        except ValueError:
            print("Invalid number of days. Please enter an integer.")
