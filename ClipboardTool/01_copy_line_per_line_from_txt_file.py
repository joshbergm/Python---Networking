import pyperclip
import keyboard
import time
import os

file_path = os.path.join("c:/Users/JoshuaBergman/OneDrive - CloudShapers/Documents/Visual Studio Code/Projecten/Python-Networking/ClipboardTool/rules.txt")

def load_lines_from_file(file_path):
    """Load lines from the text file."""
    with open(file_path, 'r') as file:
        return file.readlines()

def copy_to_clipboard(line):
    """Copy a line to the clipboard."""
    pyperclip.copy(line)

def main(file_path):
    lines = load_lines_from_file(file_path)
    
    print("Press Ctrl+V to paste the next rule.")
    
    for line in lines:
        copy_to_clipboard(line)
        print(f"Copied: {line.strip()}")
        
        # Wait for Ctrl+V to be pressed
        while True:
            if keyboard.is_pressed('ctrl+v'):
                time.sleep(0.2)  # debounce the input to avoid multiple detections
                break

if __name__ == "__main__":
    main(file_path)
