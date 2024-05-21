import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
from moviepy.video import fx as vfx
import sys
import os


from Utils.ModelManager import ModelManager
from Utils import VideoProcessor
from Utils.DataManager import DataManager

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
        
        VideoProcessor.save_video(model_manager.final_frames, 'output.avi')
        
        messagebox.showinfo("Success", "Video processed and saved to 'output.avi'")

        #ask the user if they want to save the processed video to database
        save_to_database = messagebox.askyesno("Save to Database", "Do you want to save the processed video to the database?")
        if save_to_database:
            
            #clear the progress bar
            progress_bar.destroy()
            progress_info.destroy()
            header.config(text="Uploading input video to file storage...")
            header.update()
            #upload the input and output files to pixeldrain
            input_file_link = DataManager.upload_needed_files(input_path_global)
            
            header.config(text="Uploading output video to file storage...")
            header.update()
            output_file_link = DataManager.upload_needed_files('output.mp4')
            #store the links to the database
            header.config(text="Storing videos and player average speed to the database...")
            header.update()
            #read the json config file
            
            db_config = DataManager.read_json_file('config.json')
            data_manager = DataManager(db_config['databaseUri'], db_config['databaseName'])
            player1_avg_speed = 0
            player2_avg_speed = 0
            
            for i in range(len(player_spds)):
                if(len(player_spds[i]) < 2):
                    continue
                player1_avg_speed += player_spds[i][0]
                player2_avg_speed += player_spds[i][1]
            player1_avg_speed /= len(player_spds)
            player2_avg_speed /= len(player_spds)
            data_manager.store_to_database({'input_file_link': input_file_link, 'output_file_link': output_file_link, 'player1_spd': player1_avg_speed, 'player2_spd': player2_avg_speed}, db_config['collectionName'])
            messagebox.showinfo("Success", "Video saved to the database")
        # Ask the user if they want to play the video
        play_video = messagebox.askyesno("Play Video", "Do you want to play the processed video?")
        if not play_video:
            # destroy all widgets
            for widget in root.winfo_children():
                widget.destroy()
            root.quit()
            return
        


        # Play the video using the default media player
        if os.name == 'nt':  # Windows
            os.startfile('output.avi')
        elif os.name == 'posix':  # macOS or Linux
            os.system(f'open "output.avi"' if sys.platform == 'darwin' else f'xdg-open "output.avi"')
            
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