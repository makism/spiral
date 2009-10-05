#!/usr/bin/env python
"""
    Demonstrating a simple feedforward neural network.
    The hidden layers have the same number of neurons.
    
    We have 3 inputs, 1 output, and 2 hidden layers with 2 neurons each.
    
    This is the same as the "example1.py" in the "neurons" folder.
"""


# batteries
import sys
sys.path.append ("../../src/")
# spiral framework
from spiral.helper import colored
from spiral.nn import globals
from spiral.nn.impl import Feedforward
 

if __name__ == "__main__":
    globals.runInDebug = False
    
    settings = {
        "Inputs" : 3,
        "Outputs": 1,
        "Layers" : 2,
        "NeuronsPerLayer": 2,
        "AddBias": True
    }
    
    nn = Feedforward (**settings)
    nn.createNet ()
    nn.createDefaultSynapses ()
    
    inputs = [ 1.0, 2.0, 3.0 ]
    weights= [ 0.3, 0.4, -0.1, -0.8, -0.25, 0.25, \
               1.0, 0.8,  0.7,  0.1, \
               0.1, 0.2, 1.0, 0.3, 0.24, 0.324, 0.12 ]
    
    nn.update (inputs, weights)
    print "Neural Network epoch completed in: %r seconds" % nn.timeUpdate ()
    print colored ("Neural Network output: %r", fg="yellow") % nn.output (0)
    
