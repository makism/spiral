#!/usr/bin/env python
"""
    Input layer connects with the first hidden layer and the output layer as well.
    The "network" is really simple since it is composed only of three neurons.
"""


# batteries
import sys
sys.path.append ("../../src/")
# spiral framework
from spiral.nn import globals
from spiral.nn.generic import Neuron
from spiral.helper import colored

 

if __name__ == "__main__":
    globals.runInDebug = False
    
    n1 = Neuron (Id=1, LayerId=0, Name="Input")
    n2 = Neuron (Id=2, LayerId=1)
    n3 = Neuron (Id=3, LayerId=2, Name="Output")
    
    # Create the synapses
    n1.createSynapse (1, n2)
    n1.createSynapse (1, n3)
    n2.createSynapse (2, n3)
    
    # Put the weights
    n1.putWeights ((0.5, 3.0))
    n2.putWeights ((-.75,))
    
    # Insert the inputs
    n1.putInput (1.0)
    
    print colored ("Output value: %r", fg="yellow") % n3.getValue ()
    
