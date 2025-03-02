import tkinter as tk
from tkinter import filedialog, messagebox

# Known platform signatures in Unity AssetBundles
PLATFORM_SIGNATURES = {
    "StandaloneWindows 5": b"\x05\x00\x00\x00",  # Windows platform ID for Unity 5.5.5f1
    "StandaloneWindows64 19": b"\x13\x00\x00\x00",  # Windows 64-bit platform ID
    "Android": b"\x0D\x00\x00\x00",  # Android platform ID
}

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
    file_path = filedialog.askopenfilename(filetypes=[("AssetBundle Files", "*.unity3d")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

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

tk.Label(root, text="Enter Bundle ID:").pack()
entry_bundle_id = tk.Entry(root, width=50)
entry_bundle_id.pack()

tk.Label(root, text="Select Current Platform:").pack()
platform_var_current = tk.StringVar(value="StandaloneWindows 5")
tk.OptionMenu(root, platform_var_current, "StandaloneWindows 5", "StandaloneWindows64 19").pack()

tk.Label(root, text="Select Target Platform:").pack()
platform_var_target = tk.StringVar(value="Android")
tk.OptionMenu(root, platform_var_target, "Android").pack()

tk.Label(root, text="Warning: This tool only works for Unity 5.5.5f1 AssetBundles!", fg="red").pack()

tk.Button(root, text="Convert", command=convert_bundle).pack()

root.mainloop()
