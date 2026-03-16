from typing import List
from actor import Actor
import copy

class Prey(Actor):
    id_counter = 0
    def __init__(
                    self,
                    curr_position: List[float] = None,
                    dimension: int = 1,
                    is_alive: bool = True,
                    visibility_radius: int = None,
                    distance_traveled: float = 0,
                    age: int = 0,
                    strategy: int = 0,
                    reproductive_energy: int = 0,
                    num_offspring: int = 0,
                    survival_time: int = 0,
                    velocity: float = 1,
                    erraticness: float = 1
                ):
        super().__init__(curr_position, dimension, is_alive, visibility_radius,
                         distance_traveled, age, strategy, reproductive_energy,
                         num_offspring, survival_time, velocity, erraticness,
                         "prey")

        self.id = Prey.id_counter
        Prey.id_counter += 1
    
    def reproduce(self, other_parent):
        # reset reproductive energy
        self.reproductive_energy = 0
        other_parent.reproductive_energy = 0
        child = copy.deepcopy(self)
        child.id = Prey.id_counter
        Prey.id_counter += 1
        # child is born at midpoint between two parents
        for i in range(self.dimension):
            child.curr_position[i] = (self.curr_position[i] + other_parent.curr_position[i]) / 2
        return child