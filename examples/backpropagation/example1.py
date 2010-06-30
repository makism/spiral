#!/usr/bin/env python
"""

"""


# batteries
import sys
sys.path.append ("../../src/")
# spiral framework
from spiral.helper import colored
from spiral.nn.generic import SimpleMath
from spiral.nn import globals
from spiral.nn.impl import Backpropagation
 

if __name__ == "__main__":
    globals.runInDebug = False
    
    settings = {
        "Inputs" : 2,
        "Outputs": 1,
        "Layers" : 1,
        "NeuronsPerLayer": 2,
        "AddBias": True,
        "LearningRate": 0.9
    }
    
    bp = Backpropagation (**settings)
    bp.createNet ()
    bp.createDefaultSynapses ()
    
    random_weights = list ()
    for i in range (bp.NumberOfWeights):
        random_weights.append (SimpleMath.randomClamped())
    
    bp.putWeights (random_weights)
    
    print colored ("Training network for 1000 iterations ...", fg="yellow")
    print colored ("*" * 80, fg="yellow")
    for i in range (1):
        bp.train ( [0, 0], 0)
        bp.train ( [0, 1], 1)
        bp.train ( [1, 0], 1)
        bp.train ( [1, 1], 0)
    
    print
    print colored ("Testing ...", fg="yellow")
    print colored ("*" * 80, fg="yellow")
    print bp.run ([0, 0])
    print bp.run ([0, 1])
    print bp.run ([1, 0])
    print bp.run ([1, 1])
    
