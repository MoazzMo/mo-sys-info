import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import psutil
import os

# Define folder paths as constants
VNA_LOGS_PATHS = [
    "C:/MILLENSYS/VNA/MiPacs/Log/Events",
    "C:/MILLENSYS/VNA/MiPacs/PacsStoreService/logs",
    "C:/MILLENSYS/VNA/MiBroker/DcmLog",
    "C:/MILLENSYS/Sites/WorkspaceVNA/logs",
    "C:/MILLENSYS/Sites/MiVNAAdmin/logs",
    "C:/MILLENSYS/Sites/MiViewer/logs",
    "C:/MILLENSYS/Sites/MiLicenseService/logs",
    "C:/MILLENSYS/Sites/MiClinic/logs",
    "C:/MILLENSYS/Sites/MiClinic/Exception",
    "C:/MILLENSYS/Sites/MiAdmin/Exception",
    "C:/MILLENSYS/Sites/MiERP/Exception",
]

MIBROKER_LOGS_PATHS = [
    "C:/millensys/MiBroker_MiClinic/HL7/Archive/Log",
    "C:/millensys/MiBroker_MiClinic/DcmLog",
    "C:/millensys/MiBroker_MiClinic/Service_Receivied_Reports",
]

def calculate_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size

def format_size(size):
    if size >= 1e9:  # GB or more
        return f"{size / 1e9:.2f} GB"
    elif size >= 1e6:  # MB or more
        return f"{size / 1e6:.2f} MB"
    elif size >= 1e3:  # KB or more
        return f"{size / 1e3:.2f} KB"
    else:
        return f"{size} bytes"

# Function to clear logs and update log size label
def clear_logs(log_paths, success_message, error_message, log_size_label):
    try:
        for path in log_paths:
            os.system(f'del /s /q "{path}"')
        mb.showinfo("Success", success_message)
    except Exception as e:
        mb.showerror("Error", f"{error_message} - {str(e)}")

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append([partition.device, usage.total, usage.used, usage.free])
        except Exception as e:
            # Skip devices that raise exceptions
            print(f"Error accessing disk information for {partition.device}: {e}")
            continue

    return disk_info

def update_ram_info(ram_label):
    virtual_memory = psutil.virtual_memory()
    ram_label.config(text=f"RAM (  Total  /  Used  /  Free  ):\n{format_size(virtual_memory.total)} / {format_size(virtual_memory.used)} / {format_size(virtual_memory.free)}")
    ram_label.after(5000, update_ram_info)

def update_data(log_size_label, tree):
    # Calculate the size of VNA-related folders
    vna_logs_size = sum(calculate_folder_size(path) for path in VNA_LOGS_PATHS)
    mibroker_logs_size = sum(calculate_folder_size(path) for path in MIBROKER_LOGS_PATHS)
    combined_logs_size = vna_logs_size + mibroker_logs_size

    log_size_label.config(text=f"Logs Size (VNA + MiBroker): {format_size(combined_logs_size)}")

    disk_info = get_disk_info


# Create a root window
root = tk.Tk()
root.title("MO-SYS-INFO")

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0, padx=5, pady=5)

# Create a "Clear VNA Logs" button
clear_vna_logs_button = ttk.Button(button_frame, text="Clear VNA Logs", command=lambda: clear_logs(VNA_LOGS_PATHS, "VNA Logs cleared successfully.", "Error clearing VNA Logs", log_size_label))
clear_vna_logs_button.grid(row=0, column=0, padx=5, pady=5)

# Create a "Clear MiBroker Logs" button
clear_mibroker_logs_button = ttk.Button(button_frame, text="Clear MiBroker Logs", command=lambda: clear_logs(MIBROKER_LOGS_PATHS, "MiBroker Logs cleared successfully.", "Error clearing MiBroker Logs", log_size_label))
clear_mibroker_logs_button.grid(row=0, column=1, padx=5, pady=5)

# Create a frame for the log size label
log_size_frame = tk.Frame(root)
log_size_frame.grid(row=1, column=0, padx=5, pady=5)

# Create a log size label
log_size_label = ttk.Label(log_size_frame, text="")
log_size_label.grid(row=0, column=0, sticky="w")

# Create a frame for the disk information treeview
disk_info_frame = tk.Frame(root)
disk_info_frame.grid(row=2, column=0, padx=5, pady=5)

# Create a Treeview widget for hard disk information
columns = ("Partitions", "Total", "Used", "Free")
tree = ttk.Treeview(disk_info_frame, columns=columns, show="headings")
tree.heading("Partitions", text="Partitions")
tree.heading("Total", text="Total")
tree.heading("Used", text="Used")
tree.heading("Free", text="Free")

# Set column widths
tree.column("Partitions", width=200)
tree.column("Total", width=100)
tree.column("Used", width=100)
tree.column("Free", width=100)

# Add a vertical scrollbar
vsb = ttk.Scrollbar(disk_info_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

# Pack the Treeview and scrollbar
tree.grid(row=0, column=0, columnspan=2, sticky="nsew")
vsb.grid(row=0, column=2, sticky="ns")

# Update the log size label and disk information
update_data(log_size_label, tree)

# Start the mainloop
root.mainloop()
