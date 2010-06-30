"""

"""


import sys
import random
# spiral-framework
from helper.Pool import ListPool



class Genome (ListPool):
    """
    
    """
    
    __lastId = 0


    def __init__ (self, Id, ChromoSize, RandomEncoding=False, PermutationEncoding=False, Encoding=None, Fitness=.0,):
        ListPool.__init__ (self)
        
        # id
        if Id is None:
            self.Id = Genome.__nextId ()
        else:
            self.Id = Id
        
        # encoding
        if Encoding is None:
            self.Encoding = list ()
        else:
            self.Encoding = Encoding
        self._pool = self.Encoding
        
        # fitness
        self.Fitness = Fitness
        
        # track mutation
        self.isMutated = False
        
        # track crossover (if THIS genome has crossovered :P)
        self.successCrossover = False
        
        # encoding size
        self.Size = ChromoSize
        
        if RandomEncoding and not PermutationEncoding:
            self.random ()
            
        if PermutationEncoding and not RandomEncoding:
            self.permutation ()
            
    @classmethod
    def __nextId (cls):
        cls.__lastId += 1
        return cls.__lastId
                
    def random (self):
        pass
    
    def permutation (self):
        pass
    
    def test (self):
        pass

    def __cmp__ (self, otherGenome):
        if type(otherGenome) is int:
            # otherGenome == Fitness
            return cmp (self.Fitness, otherGenome)
        else:
            return cmp (self.Fitness, otherGenome.Fitness)
        
    def __eq__ (self, otherGenome):
        for i in range(0, len(self.Encoding)):
            if self.Encoding[i] != otherGenome.Encoding[i]:
                return False
        
        return True
        
    def __str__ (self):
        name = str(self.__class__.__name__)
        return name + " (id: %-6d, fit: %.6f, enc: %s)" % (self.Id, self.Fitness, `self.Encoding`)

  

class NaturalNumberGenome (Genome):
    """
    
    """
    
    NAT_MIN = 1
    NAT_MAX = 100
    
    def random (self):
        for i in range (0, self.Size):
            self.Encoding.append (
                random.randint(
                    NaturalNumberGenome.NAT_MIN,
                    NaturalNumberGenome.NAT_MAX
                )
            )
            
    def permutation (self):
        for i in range (0, self.Size):
            chromo = random.randint (
                NaturalNumberGenome.NAT_MIN,
                NaturalNumberGenome.NAT_MAX
            )
            
            while chromo in self.Encoding:
                chromo = random.randint (
                    NaturalNumberGenome.NAT_MIN,
                    NaturalNumberGenome.NAT_MAX
                )
            
            self.Encoding.append (chromo)
            
class RealNumberGenome (Genome):
    """
    
    """
    
    RE_MIN = 0.0
    RE_MAX = 1.0
    
    def random (self):
        for i in range (0, self.Size):
            self.Encoding.append (
                random.random ()
            )
    

class BinaryGenome (Genome):
    """
    
    """
    
    BITS = 1
        
    def random (self):
        for i in range (0, self.Size):
            if BinaryGenome.BITS > 1:
                word = list ()
                for x in range (0, BinaryGenome.BITS):
                    word.append (random.randint(0, 1))
                
                self.Encoding.append (word)
            else:
                self.Encoding.append (random.randint(0, 1))
    
