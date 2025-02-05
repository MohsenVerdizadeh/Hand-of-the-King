import concurrent.futures
import json
import random
import importlib
from argparse import Namespace


def simulate_game(weights):
    with open('weights.txt', "w") as file:
        json.dump(weights, file)
        file.flush()
    game = importlib.import_module("train_main")
    while True:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(game.main,
                                     Namespace(player1='test5', player2='test6', load=None, save=None, video=None)
                                     )
            try:
                result = future.result(timeout=200)
                break
            except:
                continue
    return result


def initialize_population(size):
    return [[random.uniform(0, 1) for _ in range(3)] for _ in range(size)]



def evaluate_fitness(weights):
    wins = 0
    games = 10
    for _ in range(games):
        winner = simulate_game(weights)
        if winner == 1:
            wins += 1
    with open("res.txt", "a") as file:
        file.write(str(weights) + f" : {wins}" + "\n")
    return wins / games


def select_parents(population, fitness_scores, num_parents):
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
    return sorted_population[:num_parents]


def crossover(parents, offspring_size):
    offspring = []
    for _ in range(offspring_size):
        parent1, parent2 = random.sample(parents, 2)
        child = [random.choice([p1, p2]) / 2 for p1, p2 in zip(parent1, parent2)]
        offspring.append(child)
    return offspring


def mutate(offspring, mutation_rate=0.1):
    for child in offspring:
        if random.random() < mutation_rate:
            index = random.randint(0, 2)
            child[index] += random.uniform(-0.1, 0.1)
            child[index] = max(0, min(1, child[index]))
    return offspring


def genetic_algorithm(pop_size=10, generations=3):
    with open("result.txt", "r") as file:
        population = json.load(file)[1]
    for gen in range(generations):
        fitness_scores = [evaluate_fitness(weights) for weights in population]
        parents = select_parents(population, fitness_scores, pop_size // 2)
        offspring = crossover(parents, pop_size - len(parents))
        offspring = mutate(offspring)
        population = parents + offspring
        with open("result.txt", "r") as file:
            temp = json.load(file)
        temp.append(population)
        with open("result.txt", "w") as file:
            json.dump(temp, file)
            file.flush()
        with open("res.txt", "a") as file:
            file.write("----------------------------\n")
    best_weights = max(population, key=evaluate_fitness)
    return best_weights


# Train the AI with Genetic Algorithm
best_weights = genetic_algorithm()
with open("res.txt", "a") as file:
    file.write("----------------------------\n")
    file.write(best_weights)
print("Optimized Weights:", best_weights)
