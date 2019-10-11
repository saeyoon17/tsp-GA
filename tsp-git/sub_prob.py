import numpy as np
import random
from class_def import Route, Node
from pre_process import grid_alize

# gives sorted route, depends on the orientation
def get_route(grid_node, idx, orientation):
    
    if orientation == "horizontal":
        if idx == 0:
            temp = np.array(sorted(grid_node, key= lambda node: (node.x)))
        else:
            temp = np.array(sorted(grid_node, key= lambda node: (-node.x)))
    else:
        if idx == 0:
            temp = np.array(sorted(grid_node, key= lambda node: (node.y)))
        else:
            temp = np.array(sorted(grid_node, key= lambda node: (-node.y)))
        
    return Route(temp)

# generates the first population for the grid_node
# provides idx, orientation
def first_generation(grid_node, population, idx, orientation):

    temp = []
    for i in range(population):
        temp.append(get_route(grid_node, idx, orientation))

    return np.array(temp)

# calculate the distance for every mutant
# every mutant has to be called at least once to get their distance
def score(generation):

    for e in generation:
        e.distance()

    return generation


# creates a mating_pool with elites.
# elite: number of elites, parent: number of parents
# tournament: number of mutants for selecting a parent
# elite + parent is the size of the mating_pool
def tournament_selection(generation, elite, parent, tournament):

    mating_pool = []

    for i in range(elite):
        mating_pool.append(generation[i])

    # tournament selection --> add parents
    for i in range(parent):
        tournament_pool = []
        for j in range(tournament):
            tournament_pool.append(np.random.choice(generation, 1)[0])
        winner = sorted(tournament_pool, key = lambda node: node.length)
        mating_pool.append(winner[0])
    
    return np.array(mating_pool)


# ordered-cross-over of two parents
# does not touch first, last element!
def cross_over(parent1, parent2):

    route_len = len(parent1.route)
    if route_len <= 1:
        return parent1
    
    point1_idx = random.randint(1, route_len-1)
    point2_idx = random.randint(1, route_len-1)

    min_idx = min(point1_idx, point2_idx)
    max_idx = max(point1_idx, point2_idx)

    route1 = parent1.route
    route2 = parent2.route

    # every route is contained in np.array
    route_m = route1[min_idx:max_idx+1].tolist()

    route_l = []
    route_r = []
    idx = 0

    while(idx != min_idx):
        temp = route2[idx]
        if not (route2[idx] in route_m):
            route_l.append(route2[idx])
        idx += 1

    while(idx != route_len):
        temp = route2[idx]
        if not (route2[idx] in route_m):
            route_r.append(route2[idx])
        idx += 1
    
    final = route_l + route_m + route_r

    return Route(np.array(final))

# creates the next generation
def next_gen(mating_pool, elite, population, grid_node, idx, orientation):

    next_gen = []

    for i in range(elite):
        next_gen.append(mating_pool[i])
    
    for i in range(population - elite):

        # TMI: this sometimes happen when we chop the map into too small parts
        if len(mating_pool) == 0:
            # in this case, randomly generate parents
            if orientation == "horizontal":
                parent1 = get_route(grid_node, idx, orientation)
                parent2 = get_route(grid_node, idx, orientation)
            else:
                parent1 = get_route(grid_node, idx, "vertical")
                parent2 = get_route(grid_node, idx, "vertical")

        else:
            parent1 = np.random.choice(mating_pool, 1)[0]
            parent2 = np.random.choice(mating_pool, 1)[0]

        child = cross_over(parent1, parent2)

        next_gen.append(child)

    return np.array(next_gen)

# mutates a single mutant
def mutate(mutant, mutation_rate):

    mutant = mutant.route

    if len(mutant == 1):
        return Route(mutant)

    if(random.random() < mutation_rate):
        # swap around 6 elements the chosen one 
        # does not swap first and the last one
        i = random.randrange(1, len(mutant) - 1)
        swap = int(random.randrange(max(1, i - 3), min(i + 3, len(mutant)-1)))
        node1 = mutant[i]
        node2 = mutant[swap]
        mutant[i] = node2
        mutant[swap] = node1

    return Route(mutant)

# mutate the whold generation
def mutate_generation(next_gen, m_rate):

    mutated_generation = []
    idx = 0
    mutated_generation.append(next_gen[0])
    for i in range(1, len(next_gen)):
        mutated = mutate(next_gen[i], m_rate)
        mutated_generation.append(mutated)
        idx += 1

    return np.array(mutated_generation)

# run GA
def run_ga(grid_node, first, population, elite, generation_num, idx, m_rate, orientation):

    temp = first
    for i in range(generation_num):
        temp = score(temp)
        temp = tournament_selection(temp, elite, int(population/4), int(population/4))
        temp = next_gen(temp, elite, population, grid_node, idx, orientation)
        temp = mutate_generation(temp, m_rate)
        temp = score(temp)

    return temp[0]

# run sub-problem
def run_sub_prob(nodearray, slice_num, population1, m_rate1, generation1):

    print("STEP 1:")
    cheat_sheet = grid_alize(nodearray, slice_num)
    horizontal_answer = []
    vertical_answer = []
    idx = 0
    progress_idx = 0

    for i, e in enumerate(cheat_sheet):

        progress = i / len(cheat_sheet) * 100

        if int(progress) > progress_idx*10:
            print(str(int(progress)) + " percent complete")
            progress_idx += 1

        if e == []:
            horizontal_answer.append([])
            vertical_answer.append([])
            idx += 1
            continue

        else:
            vertical_idx = i%2
            horizontal_idx = int(i/slice_num)%2

            horizontal = first_generation(e, population1, horizontal_idx, "horizontal")
            vertical = first_generation(e, population1, vertical_idx, "vertical")

            sub_horizontal = run_ga(e, horizontal, population1, int(len(e)/5), generation1, horizontal_idx, m_rate1, "horizontal")
            sub_vertical = run_ga(e, vertical, population1, int(len(e)/5), generation1,vertical_idx, m_rate1, "vertical")
            
            horizontal_answer.append(sub_horizontal)
            vertical_answer.append(sub_vertical)

            idx += 1
            
    return (horizontal_answer, vertical_answer)

