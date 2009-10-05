"""
    Selection functions
"""


import random


ELITE_GENOMES = 2



def roulette_wheel (Population):
    """
    
    """
    slice = random.random () * Population.Fitness.total
    total = 0
    genome= None
    
    for i in range (0, len(Population)):
        curr_genome = Population[i]
        
        total += curr_genome.Fitness
        
        if total > slice:
            genome = curr_genome
            break
    
    return genome


def elitism (Population, Reverse=True, NumberOfElite=None):
    """
    
    """
    genomes = list ()
    total_elite   = ELITE_GENOMES
    
    if NumberOfElite is not None:
        total_elite = NumberOfElite 
    
    p = Population.pool.values()
    p.sort (reverse=Reverse)
    
    for i in range (0, total_elite):
        genomes.append (p[i])
    
    return genomes


def tournament (Population, TournamentSize=12, testForMinFitness=False, AllowDups=True):
    """
    
    """
    fitness = None
    genome  = None
    
    for tournament in range (0, TournamentSize):
        random_genome = Population [ random.randint(0, len(Population)-1) ]
        
        if fitness is None:
            fitness = random_genome.Fitness
            genome  = random_genome
        
        if AllowDups:
            while random_genome.Id in selected:
                random_genome = Population [ random.randint(0, len(Population)-1) ]
        
        if testForMinFitness==False:
            if random_genome.Fitness > fitness:
                fitness = random_genome.Fitness
                genome  = random_genome
        else:
            if random_genome.Fitness < fitness:
                fitness = random_genome.Fitness
                genome  = random_genome
            
    return genome


def binary_tournament (Population, testForMinFitness=False):
    """
    
    """
    genome  = None

    
    g1 = Population [random.randint(0, len(Population)-1)]
    g2 = g1
    
    while g2 == g1:
        g2 = Population [random.randint(0, len(Population)-1)]
        
    
    if testForMinFitness == False:
        if g1.Fitness < g2.Fitness:
            genome = g1
        else:
            genome = g2
    else:
        if g1.Fitness > g2.Fitness:
            genome = g1
        else:
            genome = g2        

    return genome


def prop_binary_tournament (Population, lower_bound=0.5, upper_bound=1.0, testForMinFitness=False):
    """
    
    """
    genome = binary_tournament(Population, testForMinFitness)
    
    p = random.random ()
    
    if p > lower_bound and p < upper_bound:
        return genome
    else:
        return None
    
