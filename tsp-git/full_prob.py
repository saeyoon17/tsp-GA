import numpy as np
import random
from class_def import Node, Route



def first_generation(initial_sample, population):

    return np.array([initial_sample]*population)

def score(generation):

    for e in generation:
        e.distance()
    
    return sorted(generation, key = lambda node: node.length)


# creates a mating_pool with elites.
# elite: number of elites, parent: number of parents
# tournament: number of mutants for selecting a parent
# elite + parent is the size of the mating_pool
def tournament_selection(generation, elite, parent, tournament):

    mating_pool = []

    for i in range(elite):
        mating_pool.append(generation[i])

    for i in range(parent):
        tournament_pool = []
        for j in range(tournament):
            tournament_pool.append(np.random.choice(generation, 1)[0])
        winner = sorted(tournament_pool, key = lambda node: node.length)
        mating_pool.append(winner[0])
    
    return np.array(mating_pool)

# ordered-cross-over of two parents
# distance of the cross over must be larger than 300
def cross_over(parent1, parent2):

    distance = 0
    while(distance < len(parent1.route)/50):
    
        flag = len(parent1.route)
        point1_idx = random.randint(0, flag)
        point2_idx = random.randint(0, flag)

        min_idx = min(point1_idx, point2_idx)
        max_idx = max(point1_idx, point2_idx)
        distance = max_idx - min_idx

    route1 = parent1.route
    route2 = parent2.route

    # every route is contained in np.array
    if type(route1) == list:
        route_m = route1[min_idx:max_idx+1]
    else:
        route_m = route1[min_idx:max_idx+1].tolist()

    route_l = []
    route_r = []
    idx = 0

    while(idx != min_idx):
        temp = route2[idx]
        if not (route2[idx] in route_m):
            route_l.append(route2[idx])
        idx += 1

    while(idx != flag):
        temp = route2[idx]
        if not (route2[idx] in route_m):
            route_r.append(route2[idx])
        idx += 1
    
    final = route_l + route_m + route_r

    return Route(np.array(final))

# gives the nex_generation
def next_gen(mating_pool, elite, population):

    next_gen = []

    for i in range(elite):
        next_gen.append(mating_pool[i])
    

    for i in range(population - elite):
        

        parent1 = np.random.choice(mating_pool, 1)[0]
        parent2 = np.random.choice(mating_pool, 1)[0]

        child = cross_over(parent1, parent2)

        next_gen.append(child)


    return np.array(next_gen)

# mutates a single mutant
def mutate(mutant, mutation_rate):

    mutant = mutant.route
    i = random.randrange(0, len(mutant))
    if(random.random() < mutation_rate):
        swap = int(random.randrange(max(0, i-int(len(mutant)/200)), min(i + int(len(mutant)/200), len(mutant))))
        node1 = mutant[i]
        node2 = mutant[swap]
        mutant[i] = node2
        mutant[swap] = node1
    return Route(mutant)

# mutate the whole generation
def mutate_generation(next_gen, mutation_rate, elite):

    mutated_generation = []
    idx = 0
    for i in range(0, len(next_gen) -1):
        #first one does not get mutated
        if idx == 0:
            mutated_generation.append(next_gen[i])
            mutated = mutate(next_gen[i], mutation_rate)
            mutated_generation.append(mutated)
            
        else:
            mutated = mutate(next_gen[i], mutation_rate)
            mutated_generation.append(mutated)
        idx += 1

    return np.array(mutated_generation)



def run_ga(first, population, elite, generation_num, m_rate):

    print("STEP 2")
    temp = first
    for i in range(generation_num):
        
        progress = i/generation_num * 100
        print(str(progress)+ " percent complete")

        temp = score(temp)
        temp = tournament_selection(temp, elite, int(population/5), int(population/4))
        temp = next_gen(temp, elite, population)
        temp = mutate_generation(temp, m_rate, int(population/5))
        temp = score(temp)

    return temp[0]


def run_full_prob(initial_sample, population2, m_rate2, generation2):
    
    population = population2
    first = first_generation(initial_sample, population)
    answer = run_ga(first, population , int(population/4), generation2, m_rate2)
    return answer