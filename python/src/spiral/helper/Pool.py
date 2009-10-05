"""

"""



class ListPool (object):
    """ 
       
    """
    
    def __init__ (self):
        self._pool = list ()

    def __getitem__ (self, index):
        return self._pool [index]
    
    def __setitem__ (self, index, value):
        self._pool.insert (index, value)
        
        if isinstance(value, Genome):
            self.Fitness._updateFitness (value)
        
    def __delitem__ (self, index):
        del self._pool [index]
            
    def __len__ (self):
        return len(self._pool)