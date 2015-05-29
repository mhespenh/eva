import threading
import time
from Queue import Queue

DEFAULT_ACCELERATION = 0.25
DEFAULT_VELOCITY = 10

movement_queue = Queue()

class ServoMovementController(object):
    do_shutdown = False
    def __init__(self, controller_id, servo_id):
        self.controller_id = controller_id
        self.servo_id = servo_id
        self._angle = 0
        self.t = threading.Thread(target=self.run, args=())
        self.t.start()

    def run(self):
        while not self.do_shutdown or not movement_queue.empty():
            if self.do_shutdown and not movement_queue.empty():
                print('Received shutdown command.  Waiting for all movements to complete')

            movement = movement_queue.get()
            self.do_it(movement)
            movement_queue.task_done()

        print('All movements complete.  Shutting down')

    def do_it(self, m):
        while self._angle != m['target_angle']:
            if m['target_angle'] > self._angle:
                self._angle += float(m['velocity']/10.0)
                if self._angle > m['target_angle']:
                    self._angle = m['target_angle']
            if m['target_angle'] < self._angle:
                self._angle -= float(m['velocity']/10.0)
                if self._angle < m['target_angle']:
                    self._angle = m['target_angle']
            print('Cur: %s\tTarget: %s' % (self._angle, m['target_angle']))
            time.sleep(1.0/m['velocity'])


    def get_cur_angle(self):
        return self._angle

    def shutdown(self):
        self.do_shutdown = True

class Servo(object):
    acceleration = 0 #in deg/s^2
    velocity = 0 #in deg/s
    target_angle = 0
    # servo angles in degrees
    angle_max = 180
    angle_min = 0

    def __init__(self, controller_id, servo_id,
                 acceleration=DEFAULT_ACCELERATION,
                 velocity=DEFAULT_VELOCITY):
        self.acceleration = acceleration
        self.velocity = velocity
        self.movement_controller = ServoMovementController(controller_id=controller_id,
                                                           servo_id=servo_id)

    def set_target_angle(self, angle):
        if angle < self.angle_max and angle > self.angle_min:
            self.target_angle = angle
            movement = { 'target_angle': self.target_angle,
                         'velocity': self.velocity
                       }
            movement_queue.put(movement)
        else:
            raise ValueError('Requested servo angle outside allowable range')

    def get_angle(self):
        return self.movement_controller.get_cur_angle()

    def set_velocity(self, velocity):
        if velocity > 0:
            self.velocity = velocity
        else:
            raise ValueError('Velocity must be greater than 0')

    def shutdown(self):
        self.movement_controller.shutdown()
