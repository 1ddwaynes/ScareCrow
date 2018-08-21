import Serial
import MotorControl


class Sonar():
    def __init__(self):
        self.distInLeft = 0
        self.distInRight = 0
        self.MAX_DISTANCE_CM = 600
        self.MAX_DISTANCE_IN = self.MAX_DISTANCE_CM / 2.5
        self.duration = 0
        self.distance = 0
        self.leftWall = False
        self.rightWall = False
        self.sonarDistanceLeft = 0
        self.sonarDistanceRight = 0

    def getDistance(self, pulse):
        self.duration = pulse
        if (self.duration < 1740):
            self.duration = 1740

        self.distance = self.duration / 74 / 2
        return self.distance

    def checkSonar(self):
        if (self.distInLeft > self.MAX_DISTANCE_IN):
            self.distInLeft = self.MAX_DISTANCE_IN
        if (self.distInRight > self.MAX_DISTANCE_IN):
            self.distInRight = self.MAX_DISTANCE_IN
        self.sonarDistanceLeft = (self.distInLeft + self.sonarDistanceLeft) / 2
        self.sonarDistanceRight = (self.distInRight + self.sonarDistanceRight) / 2

    def getFrontLeft(self, leftDuration):
        self.distInLeft = self.getDistance(leftDuration)

        if MotorControl.turn_distance > self.distInLeft:
            self.leftWall = True

    def getFrontRight(self, rightDuration):
        self.distInRight = self.getDistance(rightDuration)

        if self.distInRight < MotorControl.turn_distance:
            self.rightWall = True
