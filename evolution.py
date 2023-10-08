import csv
import os

from player import Player
import numpy as np
from config import CONFIG
import copy
import math
import random
import threading


class Evolution():

    def __init__(self, mode):
        self.mode = mode

    # calculate fitness of players
    def calculate_fitness(self, players, delta_xs):
        for i, p in enumerate(players):
            p.fitness = delta_xs[i]

    def mutate(self, child):

        # TODO
        # child: an object of class `Player`
        randomNumber = random.random()
        if randomNumber <= 0.65:
            child.nn.W1 += np.random.normal(0, 0.2, child.nn.W1.shape)
            child.nn.W2 += np.random.normal(0, 0.2, child.nn.W2.shape)
            child.nn.b1 += np.random.normal(0, 0.2, child.nn.b1.shape)
            child.nn.b1 += np.random.normal(0, 0.2, child.nn.b2.shape)
        return child

    def crossover(self, p1, p2, r_cross):
        if random.random() < r_cross:
            p1.nn.W1, p2.nn.W1 = self.crossover_matrixes(p1.nn.W1, p2.nn.W1)
            p1.nn.W2, p2.nn.W2 = self.crossover_matrixes(p1.nn.W2, p2.nn.W2)
            p1.nn.b1, p2.nn.b1 = self.crossover_matrixes(p1.nn.b1, p2.nn.b1)

        return p1, p2

    def generate_new_population(self, num_players, prev_players=None):

        # in first generation, we create random players
        if prev_players is None:
            return [Player(self.mode) for _ in range(num_players)]

        else:

            # TODO
            # num_players example: 150
            # prev_players: an array of `Player` objects
            new_players = []
            totalFitness = 0
            chances = []
            for player in prev_players:
                totalFitness += player.fitness

            for player in prev_players:
                chances.append(player.fitness / totalFitness)

            # ***************** Todo : with `fitness proportionate` selection method
            # for i in range(len(chances)):
            #     for j in range(math.ceil(num_players * chances[i])):
            #         new_player = copy.deepcopy(prev_players[i])
            #         new_players.append(self.mutate(new_player))
            #         if len(new_players) == num_players:
            #             break
            #     if len(new_players) == num_players:
            #         break
            #
            # return new_players
            # ***************************************************************************

            # TODO (additional): a selection method other than `fitness proportionate`
            # # (1) Roulette Wheel
            # for i in range(1, len(chances)):
            #     chances[i] = chances[i - 1] + chances[i]
            #
            # for i in range(num_players):
            #     randomNumber = random.random()
            #     for j in range(len(chances)):
            #         if randomNumber < chances[j]:
            #             new_player = copy.deepcopy(prev_players[j])
            #             new_players.append(self.mutate(new_player))
            #             break
            #
            # return new_players
            # **************************************************************************
            # # (2) Random Selection
            # new_players = np.random.choice(prev_players, size=num_players, replace=True)
            # new_parents = []
            # for player in new_players:
            #     new_parents.append(self.mutate(player))
            #
            # return new_parents
            # **************************************************************************
            # # (3) Q-tournoment
            # for i in range(num_players):
            #     selected_group_players = []
            #     for j in range(5):
            #         selected_group_players.append(prev_players[random.randint(0, len(prev_players) - 1)])
            #     best_player = copy.deepcopy(max(selected_group_players, key=lambda x: x.fitness))
            #     new_players.append(self.mutate(best_player))
            #
            # return new_players
            # ***************************************************************************

            # ***************************** TODO (additional): implementing crossover
            for i in range(len(chances)):
                for j in range(math.ceil(num_players * chances[i])):
                    new_player = copy.deepcopy(prev_players[i])
                    new_players.append(new_player)
                    if len(new_players) == num_players:
                        break
                if len(new_players) == num_players:
                    break

            new_parents = []
            np.random.shuffle(new_players)
            for i in range(0, len(new_players), 2):
                p1, p2 = self.crossover(new_players[i], new_players[i + 1], 0.4)
                new_parents.append(self.mutate(p1))
                new_parents.append(self.mutate(p2))

            return new_parents
            # ***************************************************************************

    def next_population_selection(self, players, num_players, mode):

        # TODO
        # num_players example: 100
        # players: an array of `Player` objects

        # **************************************************** TODO : top-k fitness
        # players = sorted(players, key=lambda player: player.fitness, reverse=True)
        # return players[: num_players]
        # ***************************************************************************

        # ********************************************** TODO (additional): plotting
        plotting_thread = threading.Thread(target=self.write_to_file, args=(players, mode))
        plotting_thread.start()
        # ***************************************************************************

        # TODO (additional): a selection method other than `top-k`  --> Q-tournonemt
        final_players = []
        random.seed(1)
        for i in range(num_players):
            selected_group_players = []
            for j in range(5):
                selected_group_players.append(players[random.randint(0, len(players) - 1)])
            best_player = max(selected_group_players, key=lambda x: x.fitness)
            final_players.append(best_player)

        plotting_thread.join()

        return final_players
        # ***************************************************************************

    def write_to_file(self, players, mode):
        max_fitness = 0
        min_fitness = math.inf
        total_fitness = 0

        for player in players:
            total_fitness += player.fitness
            if player.fitness > max_fitness:
                max_fitness = player.fitness
            if player.fitness < min_fitness:
                min_fitness = player.fitness
        average_fitness = total_fitness / len(players)

        filename = mode + '.csv'
        if not os.path.isfile(filename):
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["max", "min", "average"])
                writer.writerow([max_fitness, min_fitness, average_fitness])
                file.close()
        else:
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([max_fitness, min_fitness, average_fitness])
                file.close()

    def crossover_matrixes(self, m1, m2):
        split_point = random.randint(1, m1.size)
        shape = m1.shape
        m1_splited_array = np.split(m1.flatten(), [split_point])
        m2_splited_array = np.split(m2.flatten(), [split_point])
        new_m1 = np.concatenate((m1_splited_array[0], m2_splited_array[1]), axis=None).reshape(shape)
        new_m2 = np.concatenate((m2_splited_array[0], m1_splited_array[1]), axis=None).reshape(shape)

        return new_m1, new_m2
