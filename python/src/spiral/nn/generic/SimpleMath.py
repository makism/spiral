"""

"""


import random



def randomClamped ():
    return random.random() - random.random()


def clamped (num, hi, lo=None):
    if lo is None:
        lo = -hi
    
    if num < lo:
        return lo
    
    if num > hi:
        return hi
    
    return num
    