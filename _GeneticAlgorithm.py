from random import randint, sample, random, shuffle
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
import seaborn as sns

# -- Variable declarations --  
tournament_size = 3

# ------------------------- #
# -- Generate population -- #
# ------------------------- #
def generate_population(population_size, initial_position, board_size):
    population = []
    initial_position = [position - 1 for position in initial_position]
    population.append(initial_position)
    # -- Generate unique candidates using list, shuffle, and checking for duplicates --
    while len(population) <= population_size:
        candidate = list(range(int(board_size)))
        shuffle(candidate)
        if candidate not in population:
            population.append(candidate)
    return population


# ---------------------- #
# -- Evaluate fitness -- #
# ---------------------- #
def fitness(candidate):
    conflict_count = 0
    for x,y in enumerate(candidate):  
        # If X = 0 we are in the first column and conflicts are not possible 
        if x != 0: 
            for i in range(x):
                previousX = x-(i+1)
                previousY = candidate[x-(i+1)]
                currentY = candidate[x]
                differenceX = x - previousX
                differenceY = abs(currentY - previousY)
                if differenceX == differenceY: 
                    conflict_count += 1
                if candidate[x] == previousY: 
                    conflict_count += 1
                    
    return conflict_count


# ---------------------------------------------------------------- #
# -- Tournament: choose the best candidate from the tournament  -- #
# ---------------------------------------------------------------- #
def selection(fitness_scores, population):
    tournament_candidates = sample(population, tournament_size) # This does a random selection of tournament_size members from our population
    winner = min(tournament_candidates, key=lambda candidate: fitness_scores[population.index(candidate)]) # This one sorts and selects the min fitness_score from the tournament candidates
    return winner


# ------------------------ #
# -- Crossover function -- #    # Crossover function collected from: https://medium.com/@samiran.bera/crossover-operator-the-heart-of-genetic-algorithm-6c0fdcb405c0
# ------------------------ #
def single_crossover(parents):

    parent_1, parent_2 = random.sample(parents, 2)
    crossover_point = random.randint(1, len(parent_1)-1)
    
    # Until two unequal parents are chosen ...  
    while np.array_equal(parent_1, parent_2): 
        parent_1, parent_2 = random.sample(parents, 2)

    parent_1_new = np.append(parent_1[:crossover_point], parent_2[crossover_point:])
    parent_2_new = np.append(parent_2[:crossover_point], parent_1[crossover_point:])

    return [parent_1_new.tolist(), parent_2_new.tolist()]


# ----------------------- #
# -- Mutation function -- #
# ----------------------- #
# TODO Make sure that the selected columns are not of the same value: no mutation happens if they are... 
def swap_mutation(offspring, mutation_rate):
    if random.random() < mutation_rate: 
        #i, j = map(int, random.sample(offspring, 2))  # Randomly select two different columns, make sure they are int! Got Type error: mutated_offspring[i], mutated_offspring[j] = mutated_offspring[j], mutated_offspring[i] TypeError: list indices must be integers or slices, not float
        i, j = random.sample(range(len(offspring)), 2)
        mutated_offspring = offspring.copy()
        mutated_offspring[i], mutated_offspring[j] = mutated_offspring[j], mutated_offspring[i]
        return mutated_offspring
    return offspring


# ------------------------------- #
# -- Evolve to next generation -- #
# ------------------------------- #
def evolve(population, mutation_rate, crossover_rate):
    parents = []
    offspring = []
    new_generation = []
    fitness_scores = [fitness(candidate) for candidate in population]

    # -- SELECTION: Select 60% of population as parents and calaculate fitness -- #
    while len(parents) <= int( len(population)*0.6): 
        tournament_winner = selection(fitness_scores, population)
        if tournament_winner not in parents:
            parents.append(tournament_winner) 
    
    parent_fitness = [fitness(parent) for parent in parents]

    # -- CROSSOVER: Apply crossover to create offspring from parents -- #
    for _ in range(len(parents)): 
        if random.random() < crossover_rate: 
            crossover = single_crossover(parents)
            for child in crossover: 
                if child not in offspring: 
                    offspring.append(child)
    
    # -- MUTATION: Apply mutation to the offspring -- #
    offspring = [swap_mutation(child, mutation_rate) for child in offspring]

    # -- EVALUATE: Evaluate the fitness of the offspring -- #
    offspring_fitness = [fitness(child) for child in offspring]

    # -- Combine the parents and the offspring and calculate fitness -- # 
    all_candidates = parents + offspring
    all_fitness_scores = parent_fitness + offspring_fitness

    combined_candidate_scores = list(zip(all_fitness_scores, all_candidates))

    # -- Sort the combined list based on fitness scores -- #
    combined_candidate_scores_sorted = sorted(combined_candidate_scores, key=lambda x: x[0])

    # -- Append the best scoring parents and children to the new generation without duplicates -- # 
    for element in combined_candidate_scores_sorted: 
        candidate = element[1]
        if candidate not in new_generation: 
            new_generation.append(element[1])

    # -- If new generation is too small, add some of the remaining candidates in the population -- # 
    if len(new_generation) < len(population):      
        for possible_parent in population: 
            if possible_parent not in new_generation: 
                new_generation.append(possible_parent)
        
    stop_index = len(population)
    new_generation = new_generation[:stop_index]

    #print("New generation: ", new_generation)
    #print("LEN new generation: ", len(new_generation))
    #print("\n\n", new_generation, "\n\n")
    return new_generation

# ------------------------------- #
# --- Linear regression plot ---- #
# ------------------------------- #

def plot_progress(fitness_scores):
    mpl.rc('figure', dpi=150)
    sns.set_style("whitegrid")
    
    num_generations = len(fitness_scores)
    plt.figure()
    
    all_X = [] # Initialize an empty list to collect all X values
    all_y = []
    
    for i, scores in enumerate(fitness_scores):
        generation = list(range(len(scores)))
        
        all_X.extend(generation) 
        all_y.extend(scores)
        
        # -- Perform linear regression for each generation --
        X = np.array(generation).reshape(-1, 1)
        y = np.array(scores)
        reg = LinearRegression().fit(X, y)
        reg_line = reg.predict(X)

        # -- Plot fitness scores for the generation --
        plt.scatter(generation, scores, marker='.', color='blue', label="Scatter Fitness" if i == 0 else "")

        # -- Store the data points for the scatter plot --
        all_X.extend(generation)
        all_y.extend(scores)
        
    # -- Perform linear regression for all data points --
    all_X = np.array(all_X).reshape(-1, 1)
    all_y = np.array(all_y)
    reg = LinearRegression().fit(all_X, all_y)
    reg_line = reg.predict(all_X)    
    
    # -- Plot a single linear regression line for all data points --
    plt.plot(all_X, reg_line, color='red', label="Linear Regression")

    plt.title("GA - Fitness Scores and Linear Regression")
    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
