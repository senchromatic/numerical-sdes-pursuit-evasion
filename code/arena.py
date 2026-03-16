from math import inf
from predator import Predator
from prey import Prey
import random
import numpy as np


class Arena:
    def __init__(self):
        # list of all actors ordered by ID, including both alive and dead
        self.all_predators = []
        self.all_prey = []
    
    # add an existing predator to the list of all predators
    def add_predator(self, predator):
        self.all_predators.append(predator)
    
    # add an existing prey to the list of all prey
    def add_prey(self, prey):
        self.all_prey.append(prey)
    
    def all_predators_dead(self):
        for predator in self.all_predators:
            if predator.is_alive:
                return False
        return True
     
    def all_prey_dead(self):
        for prey in self.all_prey:
            if prey.is_alive:
                return False
        return True
     
    # returns a list of all predators followed by all prey
    def get_all_actors(self):
        return self.all_predators + self.all_prey
    
    # finds the nearest alive to the given actor, excluding the actor itself (if it's in the list of other_actors)
    # returns None if no distinct neighbor is found from the list of other_actors
    def find_nearest_actor(self, actor, other_actors):
        nearest_actor = None
        min_dist = inf
        for other in other_actors:
            if not other.is_alive:
                continue
            #if actor.id == other.id:
                #continue
            distance = actor.get_distance_to_actor(other)
            if distance < min_dist:
                min_dist = distance
                nearest_actor = other
        return nearest_actor

    # finds the nearest predator to the actor (excluding the actor itself, if it is also a predator)
    # returns None if no nearest predator is found
    def find_nearest_predator(self, actor):
        return self.find_nearest_actor(actor, self.all_predators)
    
    # finds the nearest prey to the actor (excluding the actor itself, if it is also a prey)
    # returns None if no nearest prey is found
    def find_nearest_prey(self, actor):
        return self.find_nearest_actor(actor, self.all_prey)
    
    # each predator tries to catch the prey that is closest to it
    def predators_attack_prey(self, exponential_threshold, step_index):
        for i, predator in enumerate(self.all_predators):
            if not predator.is_alive:
                continue
            if self.all_prey_dead():
                continue
            nearest_prey = self.find_nearest_prey(predator)
            if nearest_prey is None:
                continue
            if np.random.exponential(1 / predator.get_distance_to_actor(nearest_prey)) > exponential_threshold:
                predator.eat(nearest_prey)
                print("at time", step_index, ": predator ", i, "(", predator.curr_position, ") captured prey", nearest_prey.id, "at (", nearest_prey.curr_position, ")")
    
    def print_predators_coordinates(self):
        print("Predator coordinates:", [predator.curr_position for predator in self.all_predators])

    def print_prey_coordinates(self):
        print("Prey coordinates:", [prey.curr_position for prey in self.all_prey])
    
    def randomly_place_new_predator(self, num_dimensions, random_scatter, strategy):
        random_gaussian_location = [np.random.normal(scale=random_scatter) for i in range(num_dimensions)]
        self.add_predator(Predator(curr_position=random_gaussian_location, dimension=num_dimensions, strategy=strategy))
    
    def randomly_place_new_prey(self, num_dimensions, random_scatter, strategy):
        random_gaussian_location = [np.random.normal(scale=random_scatter) for i in range(num_dimensions)]
        self.add_prey(Prey(curr_position=random_gaussian_location, dimension=num_dimensions, strategy=strategy))
    
    def reproduce_predators(self, min_energy, reproduction_threshold, step_index):
        new_predators = []
        for i, predator1 in enumerate(self.all_predators):
            if not (predator1.is_alive and predator1.reproductive_energy > min_energy):
                continue
            shuffled_predators = list(enumerate(self.all_predators))
            random.shuffle(shuffled_predators)
            for j, predator2 in shuffled_predators:
                if i >= j:
                    continue
                if not (predator2.is_alive and predator2.reproductive_energy > min_energy):
                    continue
                if np.random.exponential(1 / predator1.get_distance_to_actor(predator2)) > reproduction_threshold:
                    new_predators.append(predator1.reproduce(predator2))
                    print("at time", step_index, ": predator", i, "(", predator1.curr_position, ") reproduced with predator", j, "(", predator2.curr_position, ")")
                    predator1.num_offspring += 1
                    predator2.num_offspring += 1
                    break  # exit loop after resetting reproductive energy
        self.all_predators.extend(new_predators)
    
    def reproduce_prey(self, min_energy, reproduction_threshold, step_index):
        new_prey = []
        for i, prey1 in enumerate(self.all_prey):
            if not (prey1.is_alive and prey1.reproductive_energy > min_energy):
                continue
            shuffled_prey = list(enumerate(self.all_prey))
            random.shuffle(shuffled_prey)
            for j, prey2 in shuffled_prey:
                if i >= j:
                    continue
                if not (prey2.is_alive and prey2.reproductive_energy > min_energy):
                    continue
                if np.random.exponential(1 / prey1.get_distance_to_actor(prey2)) > reproduction_threshold:
                    new_prey.append(prey1.reproduce(prey2))
                    print("at time", step_index, ": prey", i, "(", prey1.curr_position, ") reproduced with prey", j, "(", prey2.curr_position, ")")
                    prey1.num_offspring += 1
                    prey2.num_offspring += 1
                    break  # exit loop after resetting reproductive energy
        self.all_prey.extend(new_prey)

