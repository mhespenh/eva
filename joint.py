import servo

class Joint:
    name = "joint"
    _servo = None
    _max_angle = 180
    _min_angle = 0
    def __init__(self, name, controller_id, servo_id, max_angle, min_angle):
        self.name = name
        self._max_angle = max_angle
        self._min_angle = min_angle
        self._servo = servo.Servo(controller_id=controller_id,
                                  input_id=servo_id)

    def set_angle(self, angle, speed=False):
        if speed:
            self._servo.set_velocity(speed)
        self._servo.set_target_angle(angle)

    def get_target_angle(self):
        return self._servo.get_target_angle()

    def get_angle(self):
        return self._servo.get_angle()