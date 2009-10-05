"""

"""


from ga.Genome import Genome



class _FitnessCache (object):
    scores= dict ()
    
    def __init__ (self):
        self.hits  = 0
        self.misses= 0
    
    def convert (self, Genome):
        key = ""
        
        for chromo in Genome:
            key += `chromo`
            
        return key    
    
    def load (self, Genome):
        key = self.convert (Genome)
        
        if key in _FitnessCache.scores.keys ():
            self.hits += 1
            return _FitnessCache.scores [key]
        else:
            self.misses += 1
            return None
    
    def store (self, Encoding, Score):
        key = self.convert (Encoding)
        _FitnessCache.scores[key] = Score


class Fitness (_FitnessCache):
    """
        Fitness
    """
    
    def __init__ (self):
        _FitnessCache.__init__ (self)
        
        self.total = 0.0
        self.max = 0.0
        self.avg = 0.0
        self.min = 0.0
        self.samples = 0
        self.maxScoreGenome = None
        self.minScoreGenome = None
        
    def isWorst (self, score):
        pass
    
    def isBest (self, score):
        pass
    
    def isAvg (self, score):
        pass
    
    def calculateFitness (self, Subject):
        pass
        
    def _updateFitness (self, Subject):
        self.samples += 1 
        score = Subject.Fitness
        
        if self.samples == 1:
            self.max = score
            self.min = score
            self.avg = score
        
        if score >= self.max:
            self.max = score
            self.bestGenome = Subject
        
        if score <= self.min:
            self.min = score
            self.worstGenome = Subject
            
        self.total += score
        
        self.avg = self.total / self.samples
        

class Pool (object):
    """ 
       
    """
    
    def __init__ (self):
        self._pool = dict ()

    def __getitem__ (self, index):
        if index in self._pool.keys ():
            return self._pool [index]
    
    def __setitem__ (self, index, value):
        self._pool[index] = value
        
        if isinstance(value, Genome):
            self.Fitness._updateFitness (value)
        
    def __delitem__ (self, index):
        if index in self._pool.keys ():
            del self._pool [index]
            
    def __len__ (self):
        return len(self._pool)


class Population (Pool):
    """
        Genome Population
    """
    
    # Auto-increment instance id.
    __lastId = -1
    
    def __init__ (self, Id=-1, idName=None):
        Pool.__init__ (self)
        
        self.Fitness = Fitness ()
        
        if Id != -1:
            self.Id = Id
        else:
            self.Id   = Population.__nextId()
        
        self.Mutations = 0
        
        self.Crossovers = 0
        
        self.Migrations = 0
        
        if idName is None:
            self.Name = ""
        else:
            self.Name = idName
    
    @classmethod
    def __nextId (cls):
        """
            Keeps track  of the total instances of this class (like a counter).
        """
        cls.__lastId += 1
        return cls.__lastId
    
    def __str__ (self):
        return "Population (id: %-5d, name: %s)" % (self.Id, self.Name)
