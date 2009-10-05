"""


"""


# spiral framework
from spiral.nn.generic import SimpleMath
from spiral.nn.generic import StepActivation
from spiral.nn.impl import Feedforward



class Backpropagation (Feedforward):
    
    
    def __init__ (self, Inputs, Outputs, AddBias=True, Layers=None, NeuronsPerLayer=None, Name="", LearningRate=1.0):
        Feedforward.__init__ (self, Inputs, Outputs, Layers=Layers, NeuronsPerLayer=NeuronsPerLayer, AddBias=True, StepActivation=None, Name=Name)
        
        # Learning rate
        self.LearningRate = LearningRate
        
        # Deltas
        self.Deltas = list ()
        
        # Weights
        self.Weights = list ()
    
    def _calculateDeltas (self):
        pass
        
    def putWeights (self, weights):
        self._putWeights (weights)
    
    def createNet (self):
        Feedforward.createNet (self)
        
    def train (self, Inputs, Output):
        Feedforward.update (self, Inputs, self.Weights)
        self._calculateDeltas ()
    
    def run (self, Inputs):
        pass        
    
