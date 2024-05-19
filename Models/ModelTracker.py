from ultralytics import YOLO
import cv2
import pickle
import os
class ModelTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        
    def track_frame(self, frame, classes = 0) : 
        results = self.model.track(frame, conf=0.5, persist=True, classes=classes)
        #return the coordinates of the bounding boxes, only if the confidence is above 0.5, and the class is person
        # 4 coordinates are returned: x1, y1, x2, y2
        for result in results :
            return result.boxes.xyxy.tolist()
    
    def track_frames(self, frames, useSavedPredict=True, save_path='predicted/predict.pkl', classes = 0):
        #check if the predictions are saved and the file is exist
        detections = []
        results = []
        if useSavedPredict and os.path.exists(save_path):
            with open(save_path, 'rb') as f:
                detections= pickle.load(f)
                
            for result in detections:
                results.append(result[0].boxes.xyxy.tolist())
        else:
            for frame in frames:
                detections.append(self.model.predict(frame, conf=0.5,classes=classes))
                results.append(detections[-1][0].boxes.xyxy.tolist())
            #create file to save the predictions, if directory does not exist, create it
            if not os.path.exists('predicted'):
                os.makedirs('predicted')
            with open(save_path, 'wb') as f:
                pickle.dump(detections, f)
                
        return results
        
    def predict_frame(self, frame) : 
        results = self.model.predict(frame, conf = 0.5, classes = 1)
        return results[0].boxes.xyxy.tolist()
    
    def draw_boxes(self, frame, coordinates):
        for coordinate in coordinates:
            x1, y1, x2, y2 = coordinate
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
        return frame