#!/usr/bin/python

from joint import Joint

j = Joint(name='Pinkie', controller_addr=0x40,
          servo_id=5, usec_max=2200, usec_min=800)
j.set_angle(50)
j.shutdown()
