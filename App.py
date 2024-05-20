import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
from moviepy.video import fx as vfx
import sys
import os


from Utils.ModelManager import ModelManager
from Utils import VideoProcessor
# ============== Global Variables ==============
input_path_global = None
output_path_global = None
selected_file =  False
continue_processing = True
# ============== Functions ==============
def handle_file_selection():
    input_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if not input_path:
        messagebox.showwarning("No file selected", "Please select a video file.")
        return
    input_path_global = input_path
    # Run the application
    try:
        upload_button.destroy()
        #create a progress bar
        if(input_path_global is None):
            raise Exception("No file selected")
        
        header = tk.Label(root, text="Processing video...")
        header.pack(pady=10)
        
        
        progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
        progress_bar.pack(pady=10)
        progress_bar["maximum"] = 100
        progress_bar["value"] = 0
        progress_bar.update()
        
        progress_info = tk.Label(root, text="Initing pre-trained models...")
        progress_info.pack()
        progress_info.update()
        model_manager = ModelManager(player_model_path='PretrainedModel/yolov8s.pt', court_model_path='PretrainedModel/courtModel.pt')
        model_manager.load_models()
        
        progress_info.config(text="Loading video...")
        progress_info.update()
        progress_bar["value"] = 20
        
        model_manager.load_video(input_path_global)
        
        progress_info.config(text="Running model on the video to detect players and court lines")
        progress_info.update()
        progress_bar["value"] = 30
        
        model_manager.start()
        progress_info.config(text="Drawing boxes...")
        progress_info.update()
        progress_bar["value"] = 50
        
        model_manager.draw_boxes()
        
        progress_info.config(text="Calculating player speeds...")
        progress_info.update()
        progress_bar["value"] = 70
        
        player_spds = model_manager.calculate_player_speeds()
        
        progress_info.config(text="Showing calculated player speeds...")
        progress_info.update()
        progress_bar["value"] = 90
        
        model_manager.show_calculate_player_speeds()
        
        progress_info.config(text="Saving video...")
        progress_info.update()
        progress_bar["value"] = 100
        
        VideoProcessor.save_video(model_manager.final_frames, 'output.mp4')
        
        messagebox.showinfo("Success", "Video processed and saved to 'output.mp4'")
        
        # Play the video using the default media player
        if os.name == 'nt':  # Windows
            os.startfile('output.mp4')
        elif os.name == 'posix':  # macOS or Linux
            os.system(f'open "output.mp4"' if sys.platform == 'darwin' else f'xdg-open "output.mp4"')
            
        # destroy all widgets
        for widget in root.winfo_children():
            widget.destroy()
        root.quit()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
# Initialize the main window

root = tk.Tk()
root.title("Video Upload and Process")
root.geometry("400x300")
while True : 
    input_path_global = None
    selected_file = False
    upload_button = tk.Button(root, text="Upload and Process Video", command=handle_file_selection)
    upload_button.pack(pady=20)
    root.mainloop()