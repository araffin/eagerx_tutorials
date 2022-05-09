
import eagerx
import eagerx.converters  # Registers space converters
from eagerx.utils.utils import Msg
from std_msgs.msg import Float32, Float32MultiArray


class MovingAverageFilter(eagerx.Node):
    @staticmethod
    @eagerx.register.spec("ExampleNode", eagerx.Node)
    def spec(
        spec,
        name: str,
        rate: float,
        n: int,
    ):
        """
        MovingAverage filter
        :param spec: Not provided by user.
        :param name: Node name
        :param rate: Rate at which callback is called.
        :param n: Window size of the moving average
        :return:
        """
        # Performs all the steps to fill-in the params with registered info about all functions.
        spec.initialize(MovingAverageFilter)

        # Modify default node params
        spec.config.update(name=name, rate=rate, process=eagerx.process.ENVIRONMENT, inputs=["signal"], outputs=["filtered"])
        
        # Custom node params
        # START EXERCISE 1.1
        spec.config.update(n=n)
        # START EXERCISE 1.1
        
        # Add space converters
        spec.inputs.signal.space_converter = eagerx.SpaceConverter.make("Space_Float32", -3, 3, dtype="float32")
        spec.outputs.filtered.space_converter = eagerx.SpaceConverter.make("Space_Float32MultiArray", [-3], [3], dtype="float32")
    
    # START EXERCISE 1.2
    def initialize(self, n):
        self.n = n
        self.moving_average = 0.0
    # END EXERCISE 1.2
    
    @eagerx.register.states()
    def reset(self):
        # START EXERCISE 1.3
        self.moving_average = 0.0
        # END EXERCISE 1.3

    @eagerx.register.inputs(signal=Float32)
    @eagerx.register.outputs(filtered=Float32MultiArray)
    def callback(self, t_n: float, signal: Msg):
        data = signal.msgs[-1].data
        
        # START EXERCISE 1.4
        self.moving_average = ((self.n - 1) * self.moving_average + data)/ self.n
        filtered_data = self.moving_average
        # END EXERCISE 1.4
        
        return dict(filtered=Float32MultiArray(data=[filtered_data]))
