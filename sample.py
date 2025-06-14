import os
import subprocess
import platform

def open_folder(folder_name):
    folder_paths = {
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    }

    folder_path = folder_paths.get(folder_name.lower())

    if folder_path and os.path.exists(folder_path):
        if platform.system() == "Windows":
            subprocess.run(["explorer", folder_path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", folder_path])
        print(f"✅ Opened {folder_name} folder.")
    else:
        print(f"❌ Folder '{folder_name}' not found or doesn't exist.")

# Example run:
command = input("🔊 Say: open downloads\n> ")
if "open" in command:
    folder = command.split("open")[-1].strip()
    open_folder(folder)
