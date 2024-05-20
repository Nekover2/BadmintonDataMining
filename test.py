import tkinter as tk
from tkinter import filedialog
import cv2
import PIL.ImageTk as ImageTk
from PIL import Image

# Function to handle the 'Process' button click event
def process_button_click():
    video_path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4;*.avi')])
    if video_path:
        process_video(video_path)

# Create the main window
window = tk.Tk()
window.title("Video Processing")
window.geometry("400x300")

# Create a label to display instructions
instructions_label = tk.Label(window, text="Please select a video file:")
instructions_label.pack(pady=10)

# Create a 'Process' button
process_button = tk.Button(window, text="Process", command=process_button_click)
process_button.pack(pady=10)


# windows after choosing the file
# Clear all widgets from the window
    
# Create a label to display status
status_label = tk.Label(window, text="")
status_label.pack(pady=10)

# Function to update the status label
def update_status(status):
    status_label.config(text=status)
    window.update_idletasks()
    
# Function to process the video (replace with your own processing code)

def process_video(video_path):
    
    for widget in window.winfo_children():
        widget.destroy()
    # Process the video using your code
    # Replace this with your actual processing logic
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Perform processing on the frame
        processed_frame = frame  # Placeholder, replace with your own processing logic
        # Display the processed frame
        cv2.imshow('Processed Video', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
    window.destroy()


# Start the Tkinter event loop
window.mainloop()