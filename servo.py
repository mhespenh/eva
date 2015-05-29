import threading
from time import sleep

DEFAULT_ACCELERATION = 0.25
DEFAULT_VELOCITY = 10

class Servo:
    controller_id = 0
    input_id = 0
    acceleration = 0 #in deg/s^2
    velocity = 0 #in deg/s
    angle = 0 #in degrees
    target_angle = 0
    # servo angles in degrees
    angle_max = 180
    angle_min = 0

    def __init__(self, controller_id, input_id,
                 acceleration=DEFAULT_ACCELERATION,
                 velocity=DEFAULT_VELOCITY):
        self.controller_id = controller_id
        self.input_id = input_id
        self.acceleration = acceleration
        self.velocity = velocity

    def set_target_angle(self, angle):
        if angle < self.angle_max and angle > self.angle_min:
            self.target_angle = angle
            threading.Thread(target=self._set_angle()).start()
        else:
            raise ValueError('Requested servo angle outside allowable range')

    def get_angle(self):
        return self.angle

    def get_target_angle(self):
        return self.target_angle

    def set_velocity(self, velocity):
        if velocity > 0:
            self.velocity = velocity
        else:
            raise ValueError('Velocity must be greater than 0')

    def _set_angle(self):
        while self.angle != self.target_angle:
            if self.target_angle > self.angle:
                self.angle += float(self.velocity/10.0)
                if self.angle > self.target_angle:
                    self.angle = self.target_angle
            if self.target_angle < self.angle:
                self.angle -= float(self.velocity/10.0)
                if self.angle < self.target_angle:
                    self.angle = self.target_angle
            print('Cur: %s\tTarget: %s' % (self.angle, self.target_angle))
            sleep(1.0/self.velocity)
