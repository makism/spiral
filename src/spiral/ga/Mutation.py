"""
    Mutation functions
"""


import random



MUTATION_RATE = 0.2


def exchange (Genome):
    """
    
    """
    if random.random() <= MUTATION_RATE:
        Genome.isMutated = True
        
        pos1 = random.randint(0, len(Genome.Encoding)-1)
        pos2 = pos1
        
        while pos2 == pos1:
            pos2 = random.randint(0, len(Genome.Encoding)-1)
            
        chromo1 = Genome.Encoding[pos1]
        chromo2 = Genome.Encoding[pos2]
        
        Genome.Encoding[pos1] = chromo2
        Genome.Encoding[pos2] = chromo1


def flip (Genome):
    """
    
    """
    pass


def scramble ():
    pass


def displacement ():
    pass


def insertion ():
    pass


def inversion ():
    pass


def displacement_inversion ():
    pass

