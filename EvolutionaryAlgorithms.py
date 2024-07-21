import _GeneticAlgorithm
import _AntColonyOptimization
import _BeesAlgortihm

def runGeneticAlgorithm(board_size,initial_pos,population_size,mutation_rate,crossover_rate,generations):
    board_size = int(board_size)
    initial_pos = [int(pos) for pos in initial_pos.split()]
    gen = 1
    optimal_fitness = 0 
    population = _GeneticAlgorithm.generate_population(population_size, initial_pos, board_size)
    all_fitness_scores = []
    
    while gen <= generations: 
        fitness_scores = [_GeneticAlgorithm.fitness(candidate) for candidate in population]

        if optimal_fitness not in fitness_scores:
            next_generation = _GeneticAlgorithm.evolve(population, mutation_rate, crossover_rate)
            population = next_generation.copy()
            
            # Calculate and store the fitness scores
            fitness_scores = [_GeneticAlgorithm.fitness(candidate) for candidate in population]
            all_fitness_scores.append(fitness_scores)
            print(f"Generation {gen + 1}")
            print(f"No solution was found in {gen}st generation")  
            gen += 1  
        else:
            index = fitness_scores.index(0)
            solution = population[index]
            print(f"Solution found in generation {gen} the solution is {solution}")
            ga_result = [x + 1 for x in solution]
            all_fitness_scores = list(zip(*all_fitness_scores))
            _GeneticAlgorithm.plot_progress(all_fitness_scores)
            return ga_result

# TODO Do we need to return "antgenerations"? Does not do anything now, so can remove if it is not used
def runAntColonyOptimization(n, num_ants, num_iterations, initial_pos, evaporation_rate): 
    ant_colony = _AntColonyOptimization.AntColony(n, num_ants, num_iterations, initial_pos, evaporation_rate)
    aco_result, antgenerations, all_fitness_scores = ant_colony.place_queens()
    aco_result = [x + 1 for x in aco_result]
    return aco_result


def runBeesAlgorithm(board_size, ns, nb, ne, nrb, nre, stlim):
    max_iteration = 5000
    max_score = 0
    first_boundary = [0]* board_size # If board_size = 4 -> [0,0,0,0]
    second_boundary = [board_size-1] * board_size # If board_size = 4 -> [3,3,3,3] 
    search_boundaries=(first_boundary, second_boundary)

    bees = _BeesAlgortihm.BeesAlgorithm(search_boundaries[0],search_boundaries[1], ns, nb, ne, nrb, nre, stlim)
    bees.performFullOptimisation(max_iteration=max_iteration, max_score=max_score)

    solution = bees.best_solution 
    bco_result = solution.values
    bco_result = [x +1 for x in bco_result]
    return bco_result


def runParticleSwarmOptimization(): 
    return