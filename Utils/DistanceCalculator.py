trueCourtLongerLength = 1341
trueCourtShorterLength = 610


class DistanceCalculator :
    def __init__(self, cornerCoordinates):
        self.upperLeft = cornerCoordinates[1]
        self.lowerRight = cornerCoordinates[2]
        self.cmPerPixel = trueCourtLongerLength / (self.lowerRight[0] - self.upperLeft[0])
        self.mPerPixel = self.cmPerPixel / 100
        
    def changeCorners(self, cornerCoordinates):
        self.upperLeft = cornerCoordinates[1]
        self.lowerRight = cornerCoordinates[2]
        self.cmPerPixel = trueCourtLongerLength / (self.lowerRight[0] - self.upperLeft[0])
        self.mPerPixel = self.cmPerPixel / 100
        
    def calculateDistance(self, oldCoordinate, newCoordinate) :
        x1 = oldCoordinate[0]
        y1 = oldCoordinate[1]
        x2 = newCoordinate[0]
        y2 = newCoordinate[1]
        
        #distance between two points multiplied by the scale
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 * self.mPerPixel