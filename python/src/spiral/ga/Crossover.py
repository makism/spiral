"""
    Crossover functions
"""


import random
# custom packges and modules
from ga.Genome import Genome


CROSSOVER_RATE = 0.75


def pmx (Dad, Mum, Baby1, Baby2):
    """ Partially-Mapped Exchange """
    if random.random () > CROSSOVER_RATE or Dad == Mum:
        return
    
    Dad.successCrossover = True
    Mum.successCrossover = True
    
    Baby1.Encoding = Dad.Encoding
    Baby2.Encoding = Mum.Encoding
    
    map_start = random.randint (0, len(Mum.Encoding)-2)
    map_end   = map_start
    while map_end <= map_start:
        map_end = random.randint (0, len(Mum.Encoding)-1)

    for pos in range (map_start, map_end+1):
        g1 = Dad [pos]
        g2 = Mum [pos]
        
        if g1 != g2:
            # for Baby1
            pos1 = -1
            pos2 = -1
            for i in range (0, len(Baby1.Encoding)):
                if Baby1.Encoding[i] == g1:
                    pos1 = i
                    continue
                
                if Baby1.Encoding[i] == g2:
                    pos2 = i
            
            tmp_g1 = Baby1.Encoding[pos1]
            tmp_g2 = Baby1.Encoding[pos2]
            
            Baby1.Encoding[pos1] = tmp_g2
            Baby1.Encoding[pos2] = tmp_g1
            
            # follow the same procedure for Baby2
            pos1 = -1
            pos2 = -1
            for i in range (0, len(Baby2.Encoding)):
                if Baby2.Encoding[i] == g1:
                    pos2 = i
                    continue
                
                if Baby2.Encoding[i] == g2:
                    pos2 = i
            
            tmp_g1 = Baby2.Encoding[pos1]
            tmp_g2 = Baby2.Encoding[pos2]
            
            Baby2.Encoding[pos1] = tmp_g2
            Baby2.Encoding[pos2] = tmp_g1     

def crossover ():
    pass
