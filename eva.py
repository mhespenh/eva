#!/usr/bin/python
import joint
import limb
import time, servo

arm = limb.Limb('Arm')
elbow = joint.Joint(name="Elbow", controller_id=0, servo_id=0,
                    max_angle=180, min_angle=0)
arm.add_joint(elbow)
elbow.set_angle(angle=120, velocity=30)
elbow.set_angle(angle=30, velocity=100)

arm.shutdown()