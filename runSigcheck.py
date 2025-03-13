import subprocess
import tkinter as tk
from tkinter import filedialog

def run_command(folder_path):
    # Full path to sigcheck.exe
    command = f'C:\\Users\\Jostrovski\\Downloads\\Sigcheck\\sigcheck.exe -vt "{folder_path}"'
    
    # Run the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Display the output
    output_box.delete(1.0, tk.END)  # Clear previous output
    output_box.insert(tk.END, result.stdout)  # Insert new output

def select_folder():
    folder_path = filedialog.askdirectory()  # Open folder selection dialog
    if folder_path:  # If a folder was selected
        run_command(folder_path)  # Run the command with the selected folder

# Create the main window
root = tk.Tk()
root.title("Command Runner")

# Create a button to select folder
select_button = tk.Button(root, text="Select Folder and Run Command", command=select_folder)
select_button.pack(pady=10)

# Create a text box to display output
output_box = tk.Text(root, height=15, width=80)
output_box.pack(pady=10)

# Start the GUI event loop
root.mainloop()