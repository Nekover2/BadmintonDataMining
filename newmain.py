from Utils import VideoProcessor, ModelManager

def main():
    #read video
    input_video_path = 'video.mp4'
    video_frames = VideoProcessor.read_video(input_video_path)
    
    model_manager = ModelManager.ModelManager(player_model_path='yolov8s.pt', court_model_path='PretrainedModel/courtModel.pt')
    model_manager.load_models()

    model_manager.start(video_frames)
    frames = model_manager.draw_boxes(video_frames)
    player_spds= model_manager.calculate_player_speeds(video_frames)
    print(len(player_spds))
    print(len(frames))
    frames = model_manager.show_calculate_player_speeds(frames)
    VideoProcessor.save_video(frames, 'output.mp4')
    
    
if __name__ == "__main__":
    main()