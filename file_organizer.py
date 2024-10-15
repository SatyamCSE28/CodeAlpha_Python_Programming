import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Directory to watch
source_dir = "C:\\Users\\91790\\OneDrive\\Desktop\\from"
# Directory to organize files into
# Directory to organize files into
destination_dir = "C:\\Users\\91790\\OneDrive\\Desktop\\Automation"


# Define extensions and corresponding folder names
extensions = {
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Videos': ['.mp4', '.mov', '.avi'],
    'Music': ['.mp3', '.wav'],
    'Archives': ['.zip', '.rar'],
}

class FileOrganizerHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)

            # Ensure it's a file (not a folder)
            if os.path.isfile(file_path):
                self.organize_file(file_path)

    def organize_file(self, file_path):
        _, ext = os.path.splitext(file_path)

        for folder, ext_list in extensions.items():
            if ext.lower() in ext_list:
                folder_path = os.path.join(destination_dir, folder)

                # Create folder if it doesn't exist
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Move file to corresponding folder
                shutil.move(file_path, os.path.join(folder_path, os.path.basename(file_path)))
                print(f"Moved {file_path} to {folder_path}")
                break

if __name__ == "__main__":
    event_handler = FileOrganizerHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
  