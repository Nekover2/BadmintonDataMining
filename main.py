from Utils import VideoProcessor, ModelManager

def main():
    #read video
    input_video_path = 'output.mp4'
    video_frames = VideoProcessor.read_video(input_video_path)
    
    model_manager = ModelManager.ModelManager(player_model_path='PretrainedModel/yolov8s.pt', court_model_path='PretrainedModel/courtModel.pt')
    model_manager.load_models()
    model_manager.load_video(input_video_path)

    model_manager.start()
    model_manager.draw_boxes()
    player_spds= model_manager.calculate_player_speeds()
    model_manager.show_calculate_player_speeds()
    VideoProcessor.save_video(model_manager.final_frames, 'output1.mp4')
    
    
if __name__ == "__main__":
    main()