from Models.ModelTracker import ModelTracker
from Models.CornerDetector import CornerDetector
from Utils.VideoProcessor import read_video, save_video
from Utils.PlayerFilter import filter_players, filter_players_by_corner
import os
import cv2

def main():
    #read image 
    image = cv2.imread('image.png')
    # Read video
    input_video_path = 'video.mp4'
    video_frames = read_video(input_video_path)
    
    player_tracker = ModelTracker(model_path='yolov8s.pt')
    court_tracker = ModelTracker(model_path='PretrainedModel/court.pt')
    shuttlecock_tracker = ModelTracker(model_path='PretrainedModel/best.pt')
    # for frame in video_frames:
    court_coordinates = court_tracker.predict_frame(image)[0]
    people_coordinates = player_tracker.track_frame([image])
    
    # Cut the court from the image
    x1, y1, x2, y2 = court_coordinates
    court_image = image[int(y1):int(y2), int(x1):int(x2)]

    # Detect the corners of the court
    corner_detector = CornerDetector(court_image)
    corner_coordinates = corner_detector.convert_coordiante_size([court_coordinates])
    # We will take the first 4 corners as the court corners
    #cv2.imwrite('court.png', court_image)
    image = court_tracker.draw_boxes(image, [court_coordinates])
    
    
    frames = corner_detector.draw_key_points_on_videos([image], [court_coordinates])
    
    cv2.imwrite('output1.png', frames[0])
    
    true_player_coordinates = filter_players_by_corner(people_coordinates, corner_coordinates)
    # filter out the player coordinates that are within the court, then draw the bounding boxes
    print(corner_coordinates)
    print(true_player_coordinates)
            
    image = player_tracker.draw_boxes(image, true_player_coordinates)
    #save image
    cv2.imwrite('output.png', image)


if __name__ == "__main__":
    main()