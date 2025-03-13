import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import fnmatch

def run_command(folder_path):
    # Full path to sigcheck.exe, This may need to change dependant on if sigcheck is going to be donwloaded directly into the application package
    command = f"{r'D:\Mentorship\Sigcheck\sigcheck.exe'} -vt \"{folder_path}\""
    
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
            # Check if the detection is 'Unknown'
            if vt_detection.lower() == 'unknown':
                continue  # Skip processing that files VT detection if it's unknown

            detection_numbers = vt_detection.split('/')
            if detection_numbers and len(detection_numbers[0].strip()) > 0:
                detected_count_str = detection_numbers[0].strip()
                
                # Check if the detected count is a digit
                if detected_count_str.isdigit():
                    detected_count = int(detected_count_str)
                    # if it is then check if it is greater than zero meaning that there is a virus detected on the file 
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
        # Join infected file names into a single string
        infected_files_str = "\n".join(infected_files)
        result_message = f"Virus detected in the following file(s):\n{infected_files_str}"

    #display the message box with the scan results
    messagebox.showinfo("Scan Result", result_message)

#after running once allow the user to reselect the folder to restart the test
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
output_box = tk.Text(root)
output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Make it scalable

# Start the GUI event loop
root.mainloop()