from arena import Arena
from predator import Predator
from prey import Prey
from visualization import generate_visual_1d, collect_stats
from visualization import generate_visual_2d  # TODO: not yet used
import copy
import os
from collections import defaultdict
from statistics import mean

# number of predators and prey to start with
INITIAL_NUM_PREDATORS = 1
INITIAL_NUM_PREY = 1

# this is a threshold for the exponential r.v. by which predators can catch prey
CAPTURE_THRESHOLD = 3
# thresholds for the exponential r.v. by which predators and prey can breed
PREDATORS_REPRODUCTION_THRESHOLD = 5
PREY_REPRODUCTION_THRESHOLD = 5

# need to wait at least this many units of time before each reproductive cycle
MINIMUM_REPRODUCTIVE_ENERGY_FOR_PREDATORS = 5
MINIMUM_REPRODUCTIVE_ENERGY_FOR_PREY = 5

# choose some reasonable number that allows us to run a good enough number of trials (balanced trade-off)
NUM_TRIALS = 30
MAX_SIMULATION_STEPS = 100

# R^n has dimension n and has initial actors randomly distributed with standard deviation defined by the random scatter
ARENA_DIMENSIONS = 1
RANDOM_SCATTER = ARENA_DIMENSIONS ** 2
# if an actor's coordinate goes outside the bounding box, it will be cut off by the boundary
BOUNDING_BOX = [-10, 10]

# available choices: 0 (Brownian motion), 1 (closest enemy), or 2 (centroid)
PREDATOR_STRATEGY = 1
PREY_STRATEGY = 1

SAVE_FOLDER = "visuals"


# returns a new arena with actors in random starting positions
def initialize_arena(num_predators=1, num_prey=1):
    new_arena = Arena()
    for i in range(num_predators):
        new_arena.randomly_place_new_predator(ARENA_DIMENSIONS, RANDOM_SCATTER, PREDATOR_STRATEGY)
    for i in range(num_prey):
        new_arena.randomly_place_new_prey(ARENA_DIMENSIONS, RANDOM_SCATTER, PREY_STRATEGY)
    return new_arena


# simulates the next step in the filtration
# the step index is used for logging debug information about time elapsed
def simulate_arena(arena, step_index):
    for actor in arena.get_all_actors():
        if not actor.is_alive:
            continue
        actor.survival_time += 1
        actor.random_move(arena, BOUNDING_BOX)
    arena.predators_attack_prey(CAPTURE_THRESHOLD, step_index)
    arena.reproduce_prey(PREY_REPRODUCTION_THRESHOLD, MINIMUM_REPRODUCTIVE_ENERGY_FOR_PREY, step_index)
    arena.reproduce_predators(PREDATORS_REPRODUCTION_THRESHOLD, MINIMUM_REPRODUCTIVE_ENERGY_FOR_PREDATORS, step_index)   
    return arena


if __name__ == "__main__":
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    
    data =[]
    for trial in range(NUM_TRIALS):
        print("\nSimulation trial", trial)
        Predator.id_counter = 0
        Prey.id_counter = 0
        stage_zero = initialize_arena(num_predators=INITIAL_NUM_PREDATORS, num_prey=INITIAL_NUM_PREY)
        filtration = [stage_zero]
        for step in range(MAX_SIMULATION_STEPS):
            latest_arena = filtration[-1]
            next_arena = simulate_arena(copy.deepcopy(latest_arena), step)
            filtration.append(copy.deepcopy(next_arena))
            # terminate loop if no prey remaining or no predator left alive
            if next_arena.all_prey_dead():
                print("all prey have died!")
                break
            if next_arena.all_predators_dead():
                print("all predators have died!")
                break
        if ARENA_DIMENSIONS == 1:
            generate_visual_1d(filtration, image_name=f"{SAVE_FOLDER}/1D_paths_trial{trial}.png")
        elif ARENA_DIMENSIONS == 2:
            generate_visual_2d(filtration, image_name=f"{SAVE_FOLDER}/2D_paths_trial{trial}.png")
        
        avg_survival_time, num_prey_eaten, num_prey_survived, \
            num_offspring_prey, num_offspring_predator, \
            percent_survivors = collect_stats(filtration, folder=SAVE_FOLDER, trial=trial)
        data.append([avg_survival_time, num_prey_eaten, num_prey_survived, num_offspring_prey, num_offspring_predator, percent_survivors])
        print(f"Avg survival time: {avg_survival_time}, number of prey eaten: {num_prey_eaten}, num_prey_survived: {num_prey_survived}")
        print(f"num offspring for prey: {num_offspring_prey}, num offspring for pred: {num_offspring_predator}, percent_survivors: {percent_survivors}")

    print("\n!!!SUMMARY ACROSS TRIALS!!!")
    titles = ["avg_survival_time", "num_prey_eaten", "num_prey_survived", "num_offspring_prey", "num_offspring_predator", "percent_survivors"]
    data = [*zip(*data)]

    for i, d in enumerate(data):
        print(titles[i], "=", mean(d))