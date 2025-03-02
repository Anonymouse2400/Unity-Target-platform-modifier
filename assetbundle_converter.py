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
        
def copy_bundle_id():
    pyperclip.copy(entry_bundle_id.get())
    messagebox.showinfo("Copied", "Bundle ID copied to clipboard!")

def modify_platform(asset_path, old_platform, new_platform):
    try:
        with open(asset_path, "rb") as file:
            data = file.read()
        
        if PLATFORM_SIGNATURES[old_platform] not in data:
            return "Platform signature not found. Ensure the correct platform is selected."
        
        modified_data = data.replace(PLATFORM_SIGNATURES[old_platform], PLATFORM_SIGNATURES[new_platform], 1)
        
        modified_asset_path = asset_path.replace(".unity3d", "_modified.unity3d")
        with open(modified_asset_path, "wb") as file:
            file.write(modified_data)
        
        return f"Platform changed successfully! Modified file saved as: {modified_asset_path}"
    except Exception as e:
        return str(e)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("AssetBundle Files", "*")])
    
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)
    
    bundle_id = find_bundle_id(file_path)
    entry_bundle_id.delete(0, tk.END)
    entry_bundle_id.insert(0, bundle_id)
    detected_platform = find_current_platform(file_path)
    if detected_platform not in PLATFORM_SIGNATURES:
        detected_platform = "Unknown"
    platform_var_current.set(detected_platform)

def convert_bundle():
    file_path = entry_file.get()
    bundle_id = entry_bundle_id.get()
    current_platform = platform_var_current.get()
    target_platform = platform_var_target.get()
    
    if not file_path or not bundle_id or not current_platform or not target_platform:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    
    if current_platform not in PLATFORM_SIGNATURES or target_platform not in PLATFORM_SIGNATURES:
        messagebox.showerror("Error", "Invalid platform selection!")
        return
    
    result = modify_platform(file_path, current_platform, target_platform)
    messagebox.showinfo("Result", result)
    


# GUI Setup
root = tk.Tk()
root.title("Unity 5.5.5f1 AssetBundle Platform Converter")
root.geometry("400x350")

tk.Label(root, text="Select AssetBundle:").pack()
entry_file = tk.Entry(root, width=50)
entry_file.pack()
tk.Button(root, text="Browse", command=select_file).pack()

tk.Label(root, text="Detected Bundle ID:").pack()
entry_bundle_id = tk.Entry(root, width=50)
entry_bundle_id.pack()
tk.Button(root, text="Copy Bundle ID", command=copy_bundle_id).pack()

#tk.Label(root, text="Enter Bundle ID:").pack()
#entry_bundle_id = tk.Entry(root, width=50)
#entry_bundle_id.pack()

tk.Label(root, text="Select Current Platform:").pack()
platform_var_current = tk.StringVar(value="StandaloneWindows 5")
tk.OptionMenu(root, platform_var_current, "StandaloneWindows 5", "StandaloneWindows64 19").pack()

tk.Label(root, text="Select Target Platform:").pack()
platform_var_target = tk.StringVar(value="Android")
tk.OptionMenu(root, platform_var_target, "Android").pack()

tk.Label(root, text="Warning: This tool only works for Unity 5.5.5f1 AssetBundles Shaders might not work!", fg="red").pack()

tk.Button(root, text="Convert", command=convert_bundle).pack()

root.mainloop()
