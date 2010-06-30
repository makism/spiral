"""

"""


import threading
# custom packages and modules
from ga.Genome import *
from ga.Population import *
from ga.Demographics import PopulationDemographics



class Island (threading.Thread):
    """
        A single Island
    """
    
    def __init__ (self, cId, Epochs, PopulationSize, Initialize=False):
        threading.Thread.__init__ (self, name="Island %d" % cId)
        
        # Island id
        self.cId = cId
        
        # Total epochs
        self.Epochs= Epochs
        
        # Current epoch  
        self.Epoch = 0
        
        # Population size
        self.PopulationSize = PopulationSize
        
        # Running flag
        self.isRunning = True
        
        # Paused flag
        self.isPaused  = True
        
        # Population pass
        self.populationCreated = False
        
        # Initial population
        self.initial = Population (Id=0, idName="Initial")
        
        # Keep track of the demographics
        self.Demographics = PopulationDemographics (self.Epochs, self.PopulationSize)
        
        self.currPop = self.initial
        self.prevPop = self.initial
        
        if Initialize:
            self.createInitial ()
            
    def createInitial (self):
        pass
    
    def advanceEpoch (self):
        pass
    
    def run (self):
        pass
    
    def __str__ (self):
        return "Island %d" % self.cId


class ChainIslands (threading.Thread):
    """
        Defines and handles multiple,parallel-in-execution Islands
    """
    
    def __init__ (self, Parallel, Epochs, PopulationSize, MigrationRate):
        threading.Thread.__init__ (self)
        
        # Islands list
        self.Islands = list ()
        
        # Current island
        self.currIsland = -1
        
        # Current epoch
        self.Epoch = 0
        
        # Total epochs
        self.Epochs= Epochs
        
        # Total controllers/islands
        self.Parallel = Parallel
        
        # Topology
        self.Topology = None
        
        # Population size
        self.PopulationSize = PopulationSize
        
        # Migration rate
        self.MigrationRate  = MigrationRate
        
    def run (self):
        pass
    
