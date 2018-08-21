import Sonar
import BiSerial
import time

class MotorControl():
    def __init__(self):
        self.forward = 250
        self.turn = 200
        self.reverse = 63
        self.stop = 127

        self.now_speed = 127

        self.safe_distance = 90
        self.turn_distance = 50
        self.stop_distance = 40

        self.turnDirection = 'straight'

        self.speed = None

    def moveAndAvoid(self):
        if Sonar.sonarDistanceLeft >= self.safe_distance and Sonar.sonarDistanceRight >= self.safe_distance:
            if self.turnDirection == 'straight':
                self.speed = self.forward
            else:
                self.speed = self.turn

            self.setSpeed(self.speed)

        if self.turn_distance < Sonar.sonarDistanceLeft < self.safe_distance or Sonar.sonarDistanceRight > self.turn_distance and Sonar.sonarDistanceRight < self.safe_distance:
            if self.turnDirection == 'straight':
                self.speed = self.forward
            else:
                self.speed = self.turn

            self.setSpeed(self.speed)

        if Sonar.sonarDistanceLeft < self.turn_distance or Sonar.sonarDistanceRight < self.turn_distance:

            self.setSpeed(self.turn)

        if Sonar.LeftWall is True and Sonar.RightWall is not True:
            self.turnDirection = 'right'

        elif Sonar.RightWall is True and Sonar.LeftWall is not True:

            self.turnDirection = 'left'

        else:
            if headingError <= 0:
                self.turnDirection = 'left';

            else:
                self.turnDirection = 'right';

        self.turnMotor(); #turn in the new direction

        if Sonar.sonarDistanceLeft < self.turn_distance and Sonar.sonarDistanceRight < self.stop_distance:

            self.setSpeed(self.stop)
            self.turnDirection = 'straight' # straighten up
            self.turnMotor()
            time.sleep(600)

            #Serial.println("\n\nSTOPPING\n\n")

            while Sonar.sonarDistanceLeft < self.turn_distance or Sonar.sonarDistanceRight < self.turn_distance:

                self.setSpeed(self.reverse)
                autoHornController()
                processGPS()
                currentHeading = readCompass() #get our current heading

                calcDesiredTurn();

                Sonar.checkSonar();

                #updateDisplay();
                #smartDelay(70);
                time.sleep(60)
                self.setSpeed(self.stop);

    def setSpeed(self, speed):
        BiSerial.outputStream(speed)


    def turnMotor(self):
        if self.turnDirection == 'left':
            turnLeft()
        elif self.turnDirection == 'right':
            turnRight()
        else:
            turnNeutral()
