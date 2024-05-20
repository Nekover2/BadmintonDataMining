import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    if file_path:
        
        process_video(file_path)
    root.update_idletasks()  # Update the window after file dialog closes

def process_video(file_path):
    # Replace this with your video processing logic
    print(f"Processing video: {file_path}")

root = tk.Tk()
root.title("Video Processing")

open_button = tk.Button(root, text="Open Video", command=open_file)
open_button.pack(pady=10)

root.mainloop()
