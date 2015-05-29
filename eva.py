#!/usr/bin/python
import joint
import limb

elbow = joint.Joint(name="Elbow", controller_id=0, servo_id=0,
                  max_angle=180, min_angle=0)
elbow.set_angle(120, speed=120)

arm = limb.Limb('Arm')
arm.add_joint(elbow)

print(arm.joints['Elbow'])
