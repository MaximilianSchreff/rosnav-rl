import numpy as np
import rospy

from gymnasium import spaces
from rl_utils.utils.observation_collector import DistAngleToSubgoal
from task_generator.shared import Namespace

from ...observation_space_factory import SpaceFactory
from ...utils import stack_spaces
from ..base_observation_space import BaseObservationSpace


@SpaceFactory.register("dist_angle_to_subgoal")
class DistAngleToSubgoalSpace(BaseObservationSpace):
    """
    Represents the observation space for the goal in a navigation task.

    Args:
        goal_max_dist (float): The maximum distance to the goal. Defaults to 30.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        _max_dist (float): The maximum distance to the goal.

    Methods:
        get_gym_space: Returns the Gym space for the goal observation.
        encode_observation: Encodes the goal observation.

    """

    name = "DIST_ANGLE_TO_GOAL"
    required_observations = [DistAngleToSubgoal]

    def __init__(
        self, ns: Namespace, goal_max_dist: float = 30, *args, **kwargs
    ) -> None:
        self._ns = ns
        self._max_dist = goal_max_dist
        super().__init__(*args, **kwargs)

        rospy.set_param(f"{self._ns}/follow_subgoal", True)

    def get_gym_space(self) -> spaces.Space:
        """
        Returns the Gym space for the goal observation.

        Returns:
            spaces.Space: The Gym space for the goal observation.

        """
        _spaces = (
            spaces.Box(low=0, high=self._max_dist, shape=(1,), dtype=np.float32),
            spaces.Box(low=-np.pi, high=np.pi, shape=(1,), dtype=np.float32),
        )
        return stack_spaces(*_spaces)

    def encode_observation(
        self, observation: dict, *args, **kwargs
    ) -> DistAngleToSubgoal.data_class:
        """
        Encodes the goal observation.

        Args:
            observation (dict): The observation dictionary.

        Returns:
            ndarray: The encoded goal observation.

        """
        return observation[DistAngleToSubgoal.name]