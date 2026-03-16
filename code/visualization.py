import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import os
from statistics import mean


def pad_list(a, size, pad=np.nan):
    return [pad] * (size - len(a)) + a


def generate_visual_1d(full_filtration, image_name="1D_paths.png"):
    """
    Plot of position vs time with trajectories for each predator and prey w/ legend
    """
    num_arenas = list(range(len(full_filtration)))

    prey_dict, predator_dict = create_id_position_map(full_filtration)

    for prey_id, positions in prey_dict.items():
        plt.plot(num_arenas, pad_list(positions, len(num_arenas), pad=[np.nan]), label=f"prey_{prey_id}", linestyle="-")
    for predator_id, positions in predator_dict.items():
        plt.plot(num_arenas, pad_list(positions, len(num_arenas), pad=[np.nan]), label=f"predator_{predator_id}", linestyle="-")

    plt.title("Position vs Time")
    plt.xlabel("Time")
    plt.ylabel("Position")

    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)

    plt.savefig(image_name, bbox_inches='tight')
    print("Saved:", image_name)

    plt.clf()
    plt.cla()
    plt.close()


def generate_visual_2d(full_filtration, image_name="visuals/2D_path.png"):
    """
    Plot of position path through xy plane for each predator and prey w/ legend.
    Each dot indicates an ending position.
    """
    prey_dict, predator_dict = create_id_position_map(full_filtration)

    for prey_id, positions in prey_dict.items():
        p = np.array(positions)
        plt.plot(p[:, 0], p[:, 1], label=f"prey_{prey_id}", linestyle="-")
        plt.plot(p[:, 0][-1], p[:, 1][-1], marker="o", markeredgecolor="green", markerfacecolor="green")

    for predator_id, positions in predator_dict.items():
        p = np.array(positions)
        plt.plot(p[:, 0], p[:, 1], label=f"predator_{predator_id}", linestyle="-")
        plt.plot(p[:, 0][-1], p[:, 1][-1], marker="o", markeredgecolor="blue", markerfacecolor="blue")

    plt.title("Y-coordinates vs X-coordinates")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)

    plt.savefig(image_name, bbox_inches='tight')
    print("Saved:", image_name)
    plt.clf()
    plt.cla()
    plt.close()


def create_id_position_map(full_filtration):
    """
    Helper function;
    Create a dictionary mapping from each prey and predator's ID to positions
    """
    prey_dict = defaultdict(list)
    predator_dict = defaultdict(list)

    # create a dictionary mapping from each prey and predator's ID to positions
    for arena in full_filtration:
        for prey in arena.all_prey:
            prey_dict[prey.id].append(prey.curr_position)
        for predator in arena.all_predators:
            predator_dict[predator.id].append(predator.curr_position)

    return prey_dict, predator_dict


# compute summary metrics
def collect_stats(full_filtration, folder="visuals", trial=0):
    prey_dict, predator_dict = convert_filtration_to_dicts(full_filtration)
    num_arenas = list(range(len(full_filtration)))
    make_individual_plots(num_arenas, prey_dict, predator_dict, folder=folder, trial=trial)
    avg_survival_time, num_prey_eaten, num_prey_survived, \
        num_offspring_prey, num_offspring_predator, \
        percent_survivors = make_summary_plots(num_arenas, prey_dict, predator_dict, folder=folder, trial=trial)
    return (avg_survival_time, num_prey_eaten, 
            num_prey_survived, num_offspring_prey, 
            num_offspring_predator, percent_survivors)

def make_summary_plots(num_arenas, prey_dict, predator_dict, folder="visuals", trial=0):

    plt.figure(1)
    prey = [pad_list(data["distance_traveled"], len(num_arenas)) for id, data in prey_dict.items()]
    sum_prey = [np.nansum(i) for i in zip(*prey)]
    plt.plot(num_arenas, sum_prey, label=f"prey", linestyle="-")

    pred = [pad_list(data["distance_traveled"], len(num_arenas)) for id, data in predator_dict.items()]
    sum_pred = [np.nansum(i) for i in zip(*pred)]
    plt.plot(num_arenas, sum_pred, label=f"predator", linestyle="-")

    plt.title("Total Distance Traveled vs Time")
    plt.xlabel("Time")
    plt.ylabel("Distance")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)
    path = os.path.join(folder, f"distance_total_trial{trial}.png")
    plt.savefig(path, bbox_inches='tight')
    print("Saved:", path)

    plt.clf()
    plt.cla()
    plt.close()


    plt.figure(2)
    prey = [pad_list(data["num_offspring"], len(num_arenas)) for id, data in prey_dict.items()]
    sum_prey = [np.nansum(i) for i in zip(*prey)]
    num_offspring_prey = sum_prey[-1]
    plt.plot(num_arenas, sum_prey, label=f"prey", linestyle="-")

    pred = [pad_list(data["num_offspring"],len(num_arenas))  for id, data in predator_dict.items()]
    sum_pred = [np.nansum(i) for i in zip(*pred)]
    num_offspring_predator = sum_pred[-1]
    plt.plot(num_arenas, sum_pred, label=f"predator", linestyle="-")

    plt.title("Total Number of Offspring vs Time")
    plt.xlabel("Time")
    plt.ylabel("Number of offspring")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)
    path = os.path.join(folder, f"offspring_total_trial{trial}.png")
    plt.savefig(path, bbox_inches='tight')
    print("Saved:", path)

    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(3)
    prey = [pad_list(data["is_alive"], len(num_arenas)) for id, data in prey_dict.items()]
    avg_survival_time = mean([d.count(1) for d in prey])
    sum_prey = [np.nansum(i) for i in zip(*prey)]
    num_prey_survived = sum_pred[-1]
    num_prey_eaten = len(prey_dict) - num_prey_survived
    percent_survivors = num_prey_survived / len(prey_dict)
    plt.plot(num_arenas, sum_prey, label=f"prey", linestyle="-")

    pred = [pad_list(data["is_alive"], len(num_arenas)) for id, data in predator_dict.items()]
    sum_pred = [np.nansum(i) for i in zip(*pred)]
    plt.plot(num_arenas, sum_pred, label=f"predator", linestyle="-")

    plt.title("Total Alive vs Time")
    plt.xlabel("Time")
    plt.ylabel("Alive")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)
    path = os.path.join(folder, f"alive_total_trial{trial}.png")
    plt.savefig(path, bbox_inches='tight')
    print("Saved:", path)

    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(4)
    pred = [pad_list(data["num_prey_eaten"], len(num_arenas)) for id, data in predator_dict.items()]
    sum_pred = [np.nansum(i) for i in zip(*pred)]
    plt.plot(num_arenas, sum_pred, label=f"predator", linestyle="-")

    plt.title("Total Prey Eaten vs Time")
    plt.xlabel("Time")
    plt.ylabel("Number of prey eaten")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)
    path = os.path.join(folder, f"eaten_individual_trial{trial}.png")
    plt.savefig(path, bbox_inches='tight')
    print("Saved:", path)

    plt.clf()
    plt.cla()
    plt.close()

    return (avg_survival_time, num_prey_eaten, 
            num_prey_survived, num_offspring_prey, 
            num_offspring_predator, percent_survivors)


def make_individual_plots(num_arenas, prey_dict, predator_dict, folder="visuals", trial=0):
    # make plots that show individuals first
    for prey_id, data in prey_dict.items():
        plt.figure(1)
        data_splice = pad_list(data["distance_traveled"], len(num_arenas))
        plt.plot(num_arenas, data_splice, label=f"prey{prey_id}", linestyle="-")

        plt.figure(2)
        data_splice = pad_list(data["num_offspring"], len(num_arenas))
        plt.plot(num_arenas, data_splice, label=f"prey{prey_id}", linestyle="-")

        plt.figure(3)
        data_splice = pad_list(data["is_alive"], len(num_arenas))
        plt.plot(num_arenas, data_splice, label=f"prey{prey_id}", linestyle="-")

    for pred_id, data in predator_dict.items():
        plt.figure(1)
        data_splice = pad_list(data["distance_traveled"], len(num_arenas))
        plt.plot(num_arenas, data_splice, label=f"predator{pred_id}", linestyle="-")

        plt.figure(2)
        data_splice = pad_list(data["num_offspring"], len(num_arenas))
        plt.plot(num_arenas, data_splice, label=f"predator{pred_id}", linestyle="-")

        plt.figure(3)
        data_splice =  pad_list(data["is_alive"], len(num_arenas))
        plt.plot(num_arenas, data_splice, label=f"predator{pred_id}", linestyle="-")

        plt.figure(4)
        data_splice = pad_list(data["num_prey_eaten"], len(num_arenas))
        plt.plot(num_arenas, data_splice, label=f"predator{pred_id}", linestyle="-")

    plt.figure(1)
    plt.title("Distance Traveled vs Time")
    plt.xlabel("Time")
    plt.ylabel("Distance")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)
    path = os.path.join(folder, f"distance_individual_trial{trial}.png")
    plt.savefig(path, bbox_inches='tight')
    print("Saved:", path)

    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(2)
    plt.title("Offspring vs Time")
    plt.xlabel("Time")
    plt.ylabel("Number of offspring")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)
    path = os.path.join(folder, f"offspring_individual_trial{trial}.png")
    plt.savefig(path, bbox_inches='tight')
    print("Saved:", path)

    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(3)
    plt.title("Alive vs Time")
    plt.xlabel("Time")
    plt.ylabel("Alive")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)
    path = os.path.join(folder, f"alive_individual_trial{trial}.png")
    plt.savefig(path, bbox_inches='tight')
    print("Saved:", path)

    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(4)
    plt.title("Prey Eaten vs Time")
    plt.xlabel("Time")
    plt.ylabel("Number of prey eaten")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fancybox=True,
               shadow=True, ncol=3)
    path = os.path.join(folder, f"eaten_individual_trial{trial}.png")
    plt.savefig(path, bbox_inches='tight')
    print("Saved:", path)

    plt.clf()
    plt.cla()
    plt.close()


def convert_filtration_to_dicts(full_filtration):
    prey_dict = defaultdict(lambda: defaultdict(list))
    predator_dict = defaultdict(lambda: defaultdict(list))

    for arena in full_filtration:
        for prey in arena.all_prey:
            prey_dict[prey.id]["distance_traveled"].append(prey.distance_traveled)
            prey_dict[prey.id]["num_offspring"].append(prey.num_offspring)
            prey_dict[prey.id]["strategy"].append(prey.strategy)
            prey_dict[prey.id]["is_alive"].append(int(prey.is_alive))

        for predator in arena.all_predators:
            predator_dict[predator.id]["distance_traveled"].append(predator.distance_traveled)
            predator_dict[predator.id]["num_offspring"].append(predator.num_offspring)
            predator_dict[predator.id]["num_prey_eaten"].append(predator.num_prey_eaten)
            predator_dict[predator.id]["strategy"].append(predator.strategy)
            predator_dict[predator.id]["is_alive"].append(int(predator.is_alive))

    return prey_dict, predator_dict
