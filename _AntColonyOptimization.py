import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
import seaborn as sns

class AntColony:

    # -- Initialize ant colony object. Parameters are converted to attributes. --
    # -------------------------------- #
    # -------- Initialization -------- #
    # -------------------------------- #
    def __init__(self, board_size, num_ants, num_iterations, initial_position=None, evaporation_rate=0.5, pheromone_levels=None):    
        self.board_size = int(board_size)
        initial_position = [int(pos) for pos in initial_position.split()]
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.pheromone = pheromone_levels if pheromone_levels is not None else [1] * board_size
        self.best_solution = initial_position
        self.best_conflicts = self.fitness(initial_position) if initial_position is not None else float('inf')
        self.evaporation_rate = evaporation_rate
        self.generations = 0

    # --------------------------------- #
    # ---------- Path finder ---------- #
    # --------------------------------- #
    def place_queens(self):
        self.all_fitness_scores = []
        while self.generations < self.num_iterations:
            solutions = []
            fitness_scores = []
            # -- Construct ant number of solutions --
            for ant in range(self.num_ants):
                solution = self.construct_solution() 
                # -- Store the each solution generated and its fitness score --
                solution_fitness = self.fitness(solution)
                solutions.append((solution, solution_fitness))
                fitness_scores.append(solution_fitness)
            # -- Store fitness scores for plotting --
            self.all_fitness_scores.append(fitness_scores)
            # -- Find the best solution (lowest number of conflicts) in this iteration            
            best_solution, best_conflicts = min(solutions, key=lambda x: x[1])
            
            # -- Update the global best solution if a better one is found
            if best_conflicts < self.best_conflicts:
                self.best_solution = best_solution 
                self.best_conflicts = best_conflicts
            
            # -- Update pheromone levels to solutiona and increase the generation number
            self.update_pheromone(solutions) 
            self.generations += 1

            
            
            if best_conflicts == 0:
                break

        return self.best_solution, self.generations, self.all_fitness_scores

    # --------------------------------- #
    # -------- Single Ant path -------- #
    # --------------------------------- #
    def construct_solution(self):
        solution = list(range(self.board_size))
        random.shuffle(solution)
        return solution

    # ----------------------------------------- #
    # -------- Update pheromone levels -------- #
    # ----------------------------------------- #
    def update_pheromone(self, solutions):
        
        # -- Pheromone evaporation: dependant on the evaporation rate -- 
        self.pheromone = [p * (1 - self.evaporation_rate) for p in self.pheromone] 
        
        # -- Apply pheromones to candidates based on their fitness scores --
        for solution, conflicts in solutions:
            pheromone_delta = 1 / (conflicts + 1)
            for position in solution:
                self.pheromone[position] += pheromone_delta

    # ---------------------------------- #
    # -------- Evaluate fitness -------- #
    # ---------------------------------- #
    def fitness(self, candidate):
        conflict_count = 0
        
        for x, y in enumerate(candidate):
            if x != 0:
                for i in range(x):
                    previousX = x - (i + 1)
                    previousY = candidate[x - (i + 1)]
                    currentY = candidate[x]
                    differenceX = x - previousX
                    differenceY = abs(currentY - previousY)
                    if differenceX == differenceY:
                        conflict_count += 1 # Detect diagonal conflicts
                    if candidate[x] == previousY:
                        conflict_count += 1 # Detect horizontal conflicts
    
        return conflict_count

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
        
        # Perform linear regression for each generation
        X = np.array(generation).reshape(-1, 1)
        y = np.array(scores)
        reg = LinearRegression().fit(X, y)
        reg_line = reg.predict(X)

        # Plot fitness scores for the generation
        plt.scatter(generation, scores, marker='.', color='blue', label="Scatter Fitness" if i == 0 else "")

        # Store the data points for the scatter plot
        all_X.extend(generation)
        all_y.extend(scores)
        
        # Plot linear regression line for the generation
        #plt.plot(generation, reg_line, label="Linear Regression" if i == 0 else "")

    # Perform linear regression for all data points
    all_X = np.array(all_X).reshape(-1, 1)
    all_y = np.array(all_y)
    reg = LinearRegression().fit(all_X, all_y)
    reg_line = reg.predict(all_X)    
    
    # Plot a single linear regression line for all data points
    plt.plot(all_X, reg_line, color='red', label="Linear Regression")

    plt.title("ACO - Fitness Scores and Linear Regression")
    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()