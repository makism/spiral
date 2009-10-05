#!/usr/bin/env python
"""
    In this example, we have a single neuron in the input layer, which
    connects with the hidden layer`s two neurons, which in turn, they
    connect with the output layer`s neuron.
"""


# batteries
import sys
sys.path.append ("../../src/")
# spiral framework
from spiral.nn import globals
from spiral.nn.generic import Neuron
from spiral.helper import colored

 

if __name__ == "__main__":
    globals.runInDebug = True
       
    n1 = Neuron (Id=1, LayerId=0, Name="Input")
    n1.setAutoNotify (True)
    
    n2 = Neuron (Id=2, LayerId=1)
    n3 = Neuron (Id=3, LayerId=1)
    n4 = Neuron (Id=4, LayerId=2, Name="Output")
    
    # Create the synapses
    n1.createSynapse (1, n2)
    n1.createSynapse (1, n3)
    n2.createSynapse (2, n4)
    n3.createSynapse (2, n4)
    
    print "*" * 40
    
    # Put the weights
    n1.putWeights ((0.5, 0.25))
    n2.putWeights ((-.75,))
    n3.putWeights ((1.0,))

    # Insert the inputs
    n1.putInput (1.0)


    print colored ("Output value: %r", fg="yellow") % n4.getValue ()
    
