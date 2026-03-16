# simulation entity: can be either a predator or prey
from typing import List
from abc import ABC, abstractmethod
import copy
import math
import numpy as np

class Actor(ABC):
    def __init__(
                    self,
                    curr_position: List[float] = None,
                    dimension: int = 1,
                    is_alive: bool = True,
                    visibility_radius: int = None,  # None = infinite visibility
                    distance_traveled: float = 0,
                    age: int = 0,
                    strategy: int = 0,
                    reproductive_energy: int = 0,
                    num_offspring: int = 0,
                    survival_time: int = 0,
                    velocity: float = 1,
                    erraticness: float = 1,
                    actor_type: str = ""
                ):

        self.dimension = dimension
        self.curr_position = curr_position if curr_position is not None else [0.0] * dimension
        self.is_alive = is_alive
        self.visibility_radius = visibility_radius
        self.distance_traveled = distance_traveled
        self.age = age
        self.strategy = strategy
        self.reproductive_energy = reproductive_energy
        self.num_offspring = num_offspring
        self.survival_time = survival_time
        self.velocity = velocity
        self.erraticness = erraticness
        self.actor_type = actor_type

    def random_move(self, arena, bounding_box):
        if not self.is_alive:
            return
        
        self.reproductive_energy += 1

        previous_location = self.curr_position[:]
        # strategy 0: Brownian motion
        if self.strategy == 0:
            # f(t)dBt
            for i in range(self.dimension):
                self.curr_position[i] += np.random.normal(loc=0.0, scale=self.erraticness)
        # strategy 1: chase closest prey or evade closest predator
        elif self.strategy == 1:
            # TODO: refactor with abstract methods
            # u(d(X,Y))dt | v(d(X,Y))dt
            if self.actor_type == "predator":
                nearest_prey = arena.find_nearest_prey(self)
                # TODO: vectorize with numpy array
                vector_norm = self.get_distance_to_actor(nearest_prey)
                for i in range(self.dimension):
                    self.curr_position[i] += (self.velocity / vector_norm) * (nearest_prey.curr_position[i] - self.curr_position[i])
            elif self.actor_type == "prey":
                nearest_predator = arena.find_nearest_predator(self)
                # TODO: vectorize with numpy array
                vector_norm = self.get_distance_to_actor(nearest_predator)
                for i in range(self.dimension):
                    self.curr_position[i] += (self.velocity / vector_norm) * (self.curr_position[i] - nearest_predator.curr_position[i])
        # strategy 2: escape from or pursue centroid
        elif self.strategy == 2:
            # TODO: refactor with abstract methods
            if self.actor_type == "predator":
                prey_centroid = self.find_centroid(arena.all_prey)
                vector_norm = self.get_distance_to_position(prey_centroid)
                # TODO: modularize this with the other cases in strategy 1 and 2
                for i in range(self.dimension):
                    self.curr_position[i] += (self.velocity / vector_norm) * (prey_centroid[i] - self.curr_position[i])
            elif self.actor_type == "prey":
                predators_centroid = self.find_centroid(arena.all_predators)
                vector_norm = self.get_distance_to_position(predators_centroid)
                # TODO: modularize this with the other cases in strategy 1 and 2
                for i in range(self.dimension):
                    self.curr_position[i] += (self.velocity / vector_norm) * (self.curr_position[i] - predators_centroid[i])
        else:
            raise Exception("Unknown strategy not implemented")
        # f(t)dBt
        # TODO: vectorize with numpy array
        for i in range(self.dimension):
            self.curr_position[i] += np.random.normal(loc=0.0, scale=self.erraticness)
            # check boundary conditions
            if self.curr_position[i] < bounding_box[0]:
                self.curr_position[i] = bounding_box[0] + np.random.normal()
            elif self.curr_position[i] > bounding_box[1]:
                self.curr_position[i] = bounding_box[1] - np.random.normal()

        self.distance_traveled += self.get_distance_to_position(previous_location)

    def get_distance_to_position(self, other_position):
        # TODO: implement other distance metrics
        sum_sq_dist = 0.0
        for i in range(self.dimension):
            sum_sq_dist += (self.curr_position[i] - other_position[i]) ** 2
        return math.sqrt(sum_sq_dist)

    def get_distance_to_actor(self, other_actor):
        return self.get_distance_to_position(other_actor.curr_position)

    def find_closest(self, enemy_list):
        """
        returns closest enemy object from a list of enemies;
        helper for strategy one
        """
        distances = [self.get_distance_to_actor(enemy.curr_position) for enemy in enemy_list]
        index_min = np.argmin(distances)
        return enemy_list[index_min]

    def find_centroid(self, enemy_list):
        """
        returns centroid point from a list of enemies;
        helper for strategy two
        """
        distances = np.array([enemy.curr_position for enemy in enemy_list])
        centroid = distances.mean(axis=0)
        return centroid.tolist()

    @abstractmethod
    def reproduce(self, other_parent):
        pass
