import tkinter as tk
from tkinter import filedialog, messagebox
import re
import pyperclip
import os

# Known platform signatures in Unity AssetBundles
PLATFORM_SIGNATURES = {
    "StandaloneWindows 5": b"\x05\x00\x00\x00",  # Windows platform ID for Unity 5.5.5f1
    "StandaloneWindows64 19": b"\x13\x00\x00\x00",  # Windows 64-bit platform ID
    "Android": b"\x0D\x00\x00\x00",  # Android platform ID
}

def find_bundle_id(asset_path):
    try:
        with open(asset_path, "rb") as file:
            data = file.read()
        match = re.search(rb'CAB-[a-f0-9]{32}', data)
        return match.group(0).decode('utf-8') if match else "Not Found"
    except Exception as e:
        return str(e)

def find_current_platform(asset_path):
    try:
        with open(asset_path, "rb") as file:
            data = file.read()
        for platform, signature in PLATFORM_SIGNATURES.items():
            if signature in data:
                return platform
        return "Unknown"
    except Exception as e:
        return str(e)

def modify_platform(asset_path, old_platform, new_platform):
    try:
        with open(asset_path, "rb") as file:
            data = file.read()
        
        if PLATFORM_SIGNATURES[old_platform] not in data:
            return f"Platform signature not found in {os.path.basename(asset_path)}."
        
        modified_data = data.replace(PLATFORM_SIGNATURES[old_platform], PLATFORM_SIGNATURES[new_platform], 1)
        
        with open(asset_path, "wb") as file:
            file.write(modified_data)
        
        return f"Converted: {os.path.basename(asset_path)}"
    except Exception as e:
        return f"Error processing {os.path.basename(asset_path)}: {e}"

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder_path)
        
        log_output.delete("1.0", tk.END)
        log_output.insert(tk.END, "Files to be processed:\n")
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                log_output.insert(tk.END, f"{file}\n")

def batch_convert():
    folder_path = entry_folder.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder!")
        return
    
    current_platform = platform_var_current.get()
    target_platform = platform_var_target.get()
    
    log_output.delete("1.0", tk.END)
    log_output.insert(tk.END, "Processing files:\n")
    success_count = 0
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        
        if os.path.isfile(file_path):
            if current_platform in PLATFORM_SIGNATURES:
                result = modify_platform(file_path, current_platform, target_platform)
                log_output.insert(tk.END, result + "\n")
                success_count += 1
            else:
                log_output.insert(tk.END, f"Skipping {file}: Unknown platform\n")
    
    messagebox.showinfo("Batch Conversion Complete", f"Processed {success_count} files.")

# GUI Setup
root = tk.Tk()
root.title("Batch Unity AssetBundle Converter")
root.geometry("500x500")

tk.Label(root, text="Select AssetBundle Folder:").pack()
entry_folder = tk.Entry(root, width=50)
entry_folder.pack()
tk.Button(root, text="Browse", command=select_folder).pack()

tk.Label(root, text="Select Current Platform:").pack()
platform_var_current = tk.StringVar(value="StandaloneWindows 5")
tk.OptionMenu(root, platform_var_current, "StandaloneWindows 5", "StandaloneWindows64 19").pack()

tk.Label(root, text="Select Target Platform:").pack()
platform_var_target = tk.StringVar(value="Android")
tk.OptionMenu(root, platform_var_target, "Android").pack()

tk.Label(root, text="Log Output:").pack()
log_output = tk.Text(root, height=15, width=60)
log_output.pack()

tk.Button(root, text="Convert All", command=batch_convert).pack()

tk.Label(root, text="Warning: This tool only works for Unity 5.5.5f1 AssetBundles. Shaders might not work!", fg="red").pack()

root.mainloop()
