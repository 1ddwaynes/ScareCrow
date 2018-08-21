import BiSerial
import SpeedCalculation
import time
import MotorControl


# class initGPS(threading.Thread):
class InitGPS:
    def __init__(self):
        # threading.Thread.__init__(self)

        # number of satellites detected by GPS
        self.SatN = None
        # current latitude and longitude values
        self.c_lat_value = None
        self.c_lon_value = None
        # old latitude and longitude values
        self.o_lat_value = None
        self.o_lon_value = None
        # once start default to turned on
        self.collect = True

        self._serial = BiSerial.InitSerial()

    # used to disable polling for GPS values, only necessary for polling timeouts
    def disable_GPS(self):
        collect = False

    def get_current_GPS_cord(self):
        return self.c_lat_value, self.c_lon_value

    def get_current_num_SatN(self):
        return self.SatN

    # check data for string, handshakes for certain data stream within serial buffer
    # otherwise incorrect data can be passed through causing invalid coordinate assignment
    # could possible be expanded on
    def check_instance(self, data, name):
        if data:
            if "Sat" in data:
                data = data.replace("Sat", "")
                self.SatN = float(data)
            elif "Lat" in data:
                data = data.replace("Lat", "")
                self.c_lat_value = float(data)
            elif "Lon" in data:
                data = data.replace("Lon", "")
                self.c_lon_value = float(data)

    # store passed valid cordial data for speed calculation
    def old_instance(self):
        self.o_lat_value = self.c_lat_value
        self.o_lon_value = self.c_lon_value

    # checks for repeated cord, prevents useless iteration of the speed calculation module
    def isStale(self):
        if self.c_lat_value == self.o_lat_value or self.c_lon_value == self.o_lon_value:
            return True
        else:
            return False

    # deletes/resets the current cordial data
    def reset_c(self):
        self.c_lat_value = None
        self.c_lon_value = None


    def calcOppDesiredTurn:
      # calculate where we need to turn to head to destination
      headingError = targetHeading - currentHeading # error in direction

      # adjust for compass wrap
      if (headingError < -180)
            headingError += 360
      if (headingError > 180)
            headingError -= 360

      # calculate which way to turn to intercept the targetHeading
      if abs(headingError) <= HEADING_TOLERANCE      # if within tolerance, don't turn
        MotorControl.turnDirection = 'straight'

      elif headingError < -1:

          MotorControl.turnDirection = 'right'

      elif headingError > 1:

          MotorControl.turnDirection = 'left'

      else:

          MotorControl.turnDirection = 'straight'























# Main module for GPS interfacing, could be moved to a separate modulate for possible threading implementation
def useGPS():

    # connects to serial if serial is NOT connected
    if InitGPS.connected == 0:
        InitGPS._serial.connect_Serial()

    while InitGPS.collect is True:
        #
        t_stamp1 = time.time()

        # resets GPS values if GPS values exist
        if InitGPS.c_lat_value and InitGPS.c_lon_value:
            InitGPS.reset_c()

        # main loop that reads GPS values
        while InitGPS.c_lat_value is None or GPS.c_lon_value is None:
            event_data = _serial.serial_event(str)
            if event_data is None:
                pass
            else:
                InitGPS.check_instance(event_data)
                # first time stamp to be stored, time.time() is used for linux polling
                t_stamp1 = time.time()
                #time.sleep(.5)

        # print(GPS.c_lat_value)
        # print(GPS.c_lon_value)
        # print(GPS.SatN)

        if GPS.o_lat_value is None and GPS.o_lon_value is None:
            GPS.old_instance()

        # if GPS.isStale is False:
        distance = SpeedCalculation.geod_distance(GPS.c_lat_value, GPS.c_lat_value, GPS.o_lon_value,
                                                  GPS.o_lon_value)

        t_stamp2 = time.time()
        SpeedCalculation.print_speed(t_stamp1, t_stamp2, distance)
        GPS.old_instance()
        # print(GPS.get_current_num_SatN)


# debugging
if __name__ == '__main__':
    useGPS()