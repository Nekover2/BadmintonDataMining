# use multithreading to load models
from Models.ModelTracker import ModelTracker
from Models.CornerDetector import CornerDetector
from Utils.PlayerFilter import filter_players_by_corner
from Utils.DistanceCalculator import DistanceCalculator
from Utils.VideoProcessor import read_video_attributes, read_video, save_video
import threading
import time
import os
import cv2

class ModelManager:
    def __init__(self, player_model_path='', court_model_path = '', shuttlecock_model_path = '', highest_jump = 30, save_predictions = False, save_dir = 'predicted'):
        self.player_model_path = player_model_path
        self.court_model_path = court_model_path
        self.shuttlecock_model_path = shuttlecock_model_path
        self.player_tracker = None
        self.court_tracker = None
        self.shuttlecock_tracker = None
        self.playerCoordinates = []
        self.courtCoordinates = []
        self.shuttlecockCoordinates = []
        self.cornerCoordinates = []
        self.highest_jump = highest_jump
        self.save_predictions = save_predictions
        self.save_dir = save_dir
        self.interval = 1/30
        self.player_speeds=[]
    def load_models(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        #check if model path is valid
        if os.path.exists(self.player_model_path):
            self.player_tracker = ModelTracker(model_path=self.player_model_path)
        if os.path.exists(self.court_model_path):
            self.court_tracker = ModelTracker(model_path=self.court_model_path)
            
        if os.path.exists(self.shuttlecock_model_path):
            self.shuttlecock_tracker = ModelTracker(model_path=self.shuttlecock_model_path) 
    
    def load_video(self, video_path):
        #load video
        self.width, self.height, self.fps = read_video_attributes(video_path)
        self.frames = read_video(video_path)
        self.interval = 1/self.fps
        
    def get_player_tracker(self):
        return self.player_tracker
    
    def get_court_tracker(self):
        return self.court_tracker
    
    def get_shuttlecock_tracker(self):
        return self.shuttlecock_tracker
    
    def get_player_coordinates(self):
        return self.playerCoordinates
    
    def get_court_coordinates(self):
        return self.courtCoordinates
    
    def get_shuttlecock_coordinates(self):
        return self.shuttlecockCoordinates
    
    def get_corner_coordinates(self):
        return self.cornerCoordinates
    
    def track_player(self):
        results = []
        
        for frame in self.frames:
            results.append(self.player_tracker.track_frame(frame))
        self.playerCoordinates = results
        
        
        
        
    def track_court_and_corner(self):
        courtCoordinates = []
        cornerCoordinates = []
        
        for i in range(len(self.frames)) :
            courtCoordinates.append([])
            cornerCoordinates.append([])
        #recalculate court and corner coordinates each 1 second and fill previous uncalculated frames with empty list
        frame_per_step = (int) (self.fps)
        for i in range(0, len(self.frames), frame_per_step):
            courtCoordiate = self.court_tracker.predict_frame(self.frames[i])
            if(len(courtCoordiate) > 0):
                courtCoordinates[i] = courtCoordiate[0]
                x1, y1, x2, y2 = courtCoordiate[0]
                court_image = self.frames[i][int(y1):int(y2), int(x1):int(x2)]
                corner_detector = CornerDetector(court_image)
                cornerCoordinates[i] = corner_detector.convert_coordiante_size([courtCoordiate[0]])
        
        self.courtCoordinates = courtCoordinates
        self.cornerCoordinates = cornerCoordinates
        current_court_coordinates = []
        current_corner_coordinates = []
        for i in range(0, len(self.frames), frame_per_step):
            if(len(self.cornerCoordinates[i]) != 0):
                current_court_coordinates = self.courtCoordinates[i]
                current_corner_coordinates = self.cornerCoordinates[i]
                
        for i in range(len(self.frames)) :
            if( len(self.cornerCoordinates[i]) !=0):
                current_court_coordinates = self.courtCoordinates[i]
                current_corner_coordinates = self.cornerCoordinates[i]
            self.courtCoordinates[i] = current_court_coordinates
            self.cornerCoordinates[i] = current_corner_coordinates
            
        if(len(current_corner_coordinates) == 0):
            raise Exception("Cannot detect any court corner from video, abort!")
        # for frame in self.frames:
        #     courtCoordiate = self.court_tracker.predict_frame(frame)
        #     if(len(courtCoordiate) > 0):
        #         courtCoordinates.append(courtCoordiate[0])
        #         x1, y1, x2, y2 = courtCoordiate[0]
        #         court_image = frame[int(y1):int(y2), int(x1):int(x2)]
        #         corner_detector = CornerDetector(court_image)
        #         cornerCoordinates.append(corner_detector.convert_coordiante_size([courtCoordiate[0]]))
        #     else:
        #         courtCoordinates.append([])
        #         cornerCoordinates.append([])

        # self.courtCoordinates = courtCoordinates
        # self.cornerCoordinates = cornerCoordinates
        
    def track_shuttlecock(self):
        results = []
        
        for frame in self.frames:
            results.append(self.shuttlecock_tracker.predict_frame(frame))

        self.shuttlecockCoordinates = results
        
        
    def start(self):
        #use multithreading to load models
        thread1 = None
        thread2 = None
        thread3 = None
        if(self.player_tracker is not None):
            thread1 = threading.Thread(target=self.track_player, args=())
            thread1.start()
        if(self.court_tracker is not None):
            thread2 = threading.Thread(target=self.track_court_and_corner, args=())
            thread2.start()
        if(self.shuttlecock_tracker is not None):
            thread3 = threading.Thread(target=self.track_shuttlecock, args=())
            thread3.start()
        
        if(thread1 is not None):
            thread1.join()
        if(thread2 is not None):
            thread2.join()
        if(thread3 is not None):
            thread3.join()
        
    def draw_boxes(self) :
        final_frames = []
        
            
        for i in range(len(self.frames)):
            frame = self.frames[i]
            player_coordinates = self.playerCoordinates[i]
            player_coordinates = filter_players_by_corner(player_coordinates, self.cornerCoordinates[i])
            court_coordinates = self.courtCoordinates[i]
            # shuttlecock_coordinates = self.shuttlecockCoordinates[i]
            self.playerCoordinates[i] = player_coordinates
            
            if len(court_coordinates) > 0:
                frame = self.court_tracker.draw_boxes(frame, [court_coordinates])
            if len(player_coordinates) > 0:
                
                frame = self.player_tracker.draw_boxes(frame, player_coordinates)
            # if len(shuttlecock_coordinates) > 0:
            #     frame = self.shuttlecock_tracker.draw_boxes(frame, shuttlecock_coordinates)
            
            final_frames.append(frame)
        self.boxed_frames = final_frames
        return final_frames
    
    def calculate_player_speeds(self) :
        # Calculate player speed
        self.player_speeds.append([])
        start_corner_coordinate =  []
        
        for corner in self.cornerCoordinates:
            if(len(corner) > 3) :
                start_corner_coordinate = corner
                break
        distanceCalculator = DistanceCalculator(start_corner_coordinate)
        last_coords =[]
        for i in self.playerCoordinates:
            if(len(i) > 1):
                last_coords = i
                break
        for i in range(1, len(self.frames)) :
            player_spd = []
            if(len(self.playerCoordinates[i]) < 3) :
                self.player_speeds.append(player_spd)
                continue
            for j in range(0,2):
                curr_coords = self.playerCoordinates[i][j]
                old_coords = last_coords[j]
                if(len(self.cornerCoordinates[i]) > 3) : 
                    start_corner_coordinate = self.cornerCoordinates[i]
                distanceCalculator.changeCorners(start_corner_coordinate)
                player_change = distanceCalculator.calculateDistance(oldCoordinate=old_coords, newCoordinate= curr_coords)
                player_speed = player_change/self.interval
                player_spd.append(player_speed)
                
            last_coords = self.playerCoordinates[i]
            
            self.player_speeds.append(player_spd)
        #apply abs to the player speeds and round to 2 decimal places
        for i in range(len(self.player_speeds)):
            for j in range(len(self.player_speeds[i])):
                self.player_speeds[i][j] = abs(self.player_speeds[i][j])
                self.player_speeds[i][j] = round(self.player_speeds[i][j], 2)
        return self.player_speeds

    def show_calculate_player_speeds(self) :
        # show player speed at the bottom left corner of the frame
        final_frames = []
        self.calculate_player_speeds()
        for i in range(0, len(self.frames)) :
            frame = self.frames[i]
            if(len(self.player_speeds[i]) ==0) :
                final_frames.append(frame)
                continue
            frame = self.display_player_speeds(frame,self.player_speeds[i][0], self.player_speeds[i][1])
            final_frames.append(frame)
        self.final_frames = final_frames
        return final_frames
    
    
    @staticmethod
    def display_player_speeds(frame, player1_speed, player2_speed):
    # Load the image or video frame
        
        # Set the font properties
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (255, 255, 255)  # White color

        # Define the position for player 1's speed
        player1_text = f"Player 1: {player1_speed} m/s"
        player1_text_size, _ = cv2.getTextSize(player1_text, font, font_scale, 2)
        player1_text_x = 10  # Left margin
        player1_text_y = frame.shape[0] - 10  # Bottom margin

        # Define the position for player 2's speed
        player2_text = f"Player 2: {player2_speed} m/s"
        player2_text_size, _ = cv2.getTextSize(player2_text, font, font_scale, 2)
        player2_text_x = 10  # Left margin
        player2_text_y = player1_text_y - player1_text_size[1] - 10  # Place above player 1's speed

        # Draw a filled rectangle as the background for player 1's text
        cv2.rectangle(frame, (player1_text_x, player1_text_y - player1_text_size[1]), (player1_text_x + player1_text_size[0], player1_text_y), (0, 0, 0), cv2.FILLED)

        # Draw a filled rectangle as the background for player 2's text
        cv2.rectangle(frame, (player2_text_x, player2_text_y - player2_text_size[1]), (player2_text_x + player2_text_size[0], player2_text_y), (0, 0, 0), cv2.FILLED)

        # Put player 1's text on the frame
        cv2.putText(frame, player1_text, (player1_text_x, player1_text_y), font, font_scale, font_color, 2)

        # Put player 2's text on the frame
        cv2.putText(frame, player2_text, (player2_text_x, player2_text_y), font, font_scale, font_color, 2)

        return frame