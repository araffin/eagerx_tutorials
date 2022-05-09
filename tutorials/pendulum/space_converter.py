
# ROS IMPORTS
from std_msgs.msg import Float32

# EAGERX IMPORTS
import eagerx
from eagerx.core.specs import ConverterSpec

# OTHER
import numpy as np
from gym.spaces import Box


class ExampleSpaceConverter(eagerx.SpaceConverter):
    MSG_TYPE_A = np.ndarray
    MSG_TYPE_B = Float32

    @staticmethod
    @eagerx.register.spec("ExampleSpaceConverter", eagerx.SpaceConverter)
    def spec(spec: ConverterSpec, low=None, high=None, dtype="float32"):
        # Initialize spec with default arguments
        spec.initialize(ExampleSpaceConverter)
        spec.config.update(low=low, high=high, dtype=dtype)

    def initialize(self, low=None, high=None, dtype="float32"):
        self.low = np.array(low, dtype=dtype)
        self.high = np.array(high, dtype=dtype)
        self.dtype = dtype

    def get_space(self):
        return Box(self.low, self.high, dtype=self.dtype)

    def A_to_B(self, msg):
        # In this example we only care about going from Float32 to ndarray
        raise NotImplementedError()

    def B_to_A(self, msg_b):
        th = msg_b.data
        
        # START EXERCISE 1.1
        # th -= 2 * np.pi * np.floor((th + np.pi) / (2 * np.pi))
        msg_a = np.array([np.sin(th), np.cos(th)], dtype=self.dtype)
        # END EXERCISE 1.1
        
        return msg_a
