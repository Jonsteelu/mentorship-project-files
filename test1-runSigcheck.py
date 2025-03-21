import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import fnmatch
import json

# Load the sigcheck path from a configuration file
def load_sigcheck_path():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            return config.get('sigcheck_path', '')
    return ''

# Save the selected sigcheck path to a configuration file
def save_sigcheck_path(path):
    config = {'sigcheck_path': path}
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

def run_command(folder_path):
    sigcheck_path = load_sigcheck_path()
    if not sigcheck_path or not os.path.exists(sigcheck_path):
        messagebox.showerror("Error", "Sigcheck path is not set or does not exist.")
        return
    
    # Construct the command
    command = f"{sigcheck_path} -vt \"{folder_path}\""
    
    # Run the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Clear previous output in the text box
    output_box.delete(1.0, tk.END)

    # Prepare to capture desired information
    output_lines = result.stdout.splitlines()
    relevant_output = []

    # Initialize variables to store extracted data
    file_name_path = ""
    file_date = ""
    vt_link = ""
    all_no_viruses = True  # Flag to track virus detection
    infected_files = []  # List to track files with viruses

    for line in output_lines:
        # Capture the relevant information
        if fnmatch.fnmatch(line, "?:\\*"):  # Match any drive letter that the user chooses
            file_name_path = line.strip()
        
        if "File date:" in line:
            file_date = line.split(":", 1)[1].strip()
        
        if "VT detection:" in line:
            vt_detection = line.split(":", 1)[1].strip()
            if vt_detection.lower() == 'unknown':
                continue  # Skip processing if VT detection is unknown

            detection_numbers = vt_detection.split('/')
            if detection_numbers and len(detection_numbers[0].strip()) > 0:
                detected_count_str = detection_numbers[0].strip()
                if detected_count_str.isdigit():
                    detected_count = int(detected_count_str)
                    if detected_count > 0:
                        all_no_viruses = False  # Found a virus
                        infected_files.append(file_name_path)  # Add the file to the list

        if "VT link:" in line:
            vt_link = line.split(":", 1)[1].strip()
            
            # Format the relevant output with indentation
            relevant_info = f"File Name and Path: {file_name_path}\n" \
                            f"    File Date: {file_date}\n" \
                            f"    VT Detection: {vt_detection}\n" \
                            f"    VT Link: {vt_link}\n"
            relevant_output.append(relevant_info)

    # Display only the relevant output in the text box
    if relevant_output:
        output_box.insert(tk.END, "\n".join(relevant_output))

    # Prepare the final message after displaying output
    if all_no_viruses:
        result_message = "No viruses found."
    else:
        infected_files_str = "\n".join(infected_files)
        result_message = f"Virus detected in the following file(s):\n{infected_files_str}"

    # Display the message box with the scan results
    messagebox.showinfo("Scan Result", result_message)

# Function to choose the sigcheck folder
def choose_sigcheck_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        sigcheck_path = os.path.join(folder_selected, 'sigcheck.exe')
        if os.path.exists(sigcheck_path):
            save_sigcheck_path(sigcheck_path)
            messagebox.showinfo("Settings", f"Sigcheck path set to: {sigcheck_path}")
        else:
            messagebox.showerror("Error", "sigcheck.exe not found in the selected folder.")

# Function to select folder for scanning
def select_folder():
    folder_path = filedialog.askdirectory()  # Open folder selection dialog
    if folder_path:  # If a folder was selected
        run_command(folder_path)  # Run the command with the selected folder

# Create the main window
root = tk.Tk()
root.title("Command Runner")

# Create a button to select folder for scanning
select_button = tk.Button(root, text="Select Folder and Run Command", command=select_folder)
select_button.pack(pady=10)

# Create a button for settings (to set sigcheck path)
settings_button = tk.Button(root, text="Select Sigcheck Path", command=choose_sigcheck_folder)
settings_button.pack(pady=10)

# Create a text box to display output
output_box = tk.Text(root)
output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Make it scalable

# Load existing sigcheck path if available
existing_path = load_sigcheck_path()
if existing_path:
    print(f"Existing sigcheck path: {existing_path}")

# Start the GUI event loop
root.mainloop()