import joint

class Limb:
    _name = "limb"
    joints = {}

    def __init__(self, name):
        self._name = name

    def add_joint(self, joint):
        self.joints[joint.name] = joint

    def shutdown(self):
        for j in self.joints:
            self.joints[j].shutdown()