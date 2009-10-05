#!/usr/bin/env python
"""
    The input layer has three input neurons.
    The first and second hidden layer are made of two neurons each.
    The output layer contains only one neuron.
    All the above layers are connected in a "feedforward" manner.
    
    Notice, that the number of inputs for each neuron is calculated dynamically,
    and changed whenever a new synapse-connection is created.
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
       
    n1 = Neuron (Id=1, LayerId=0)
    n2 = Neuron (Id=2, LayerId=0)
    n3 = Neuron (Id=3, LayerId=0)
    
    n4 = Neuron (Id=4, LayerId=1)
    n5 = Neuron (Id=5, LayerId=1)
    
    n6 = Neuron (Id=6, LayerId=2)
    n7 = Neuron (Id=7, LayerId=2)
    
    n8 = Neuron (Id=8, LayerId=3)
    
    # Create the synapses for input layer
    n1.createSynapse (1, n4)
    n1.createSynapse (1, n5)    
    n2.createSynapse (1, n4)
    n2.createSynapse (1, n5)
    n3.createSynapse (1, n4)
    n3.createSynapse (1, n5)
    # Create the synapses for the first hidden layer
    n4.createSynapse (2, n6)
    n4.createSynapse (2, n7)
    n5.createSynapse (2, n6)
    n5.createSynapse (2, n7)
    # Create the synapses for the second hidden layer
    n6.createSynapse (3, n8)
    n7.createSynapse (3, n8)

    # Put the weights
    n1.putWeights ( (0.3  ,  0.4) )
    n2.putWeights ( (-0.1 , -0.8) )
    n3.putWeights ( (-0.25,  0.25))
    
    n4.putWeights ( (1.0, 0.8) )
    n5.putWeights ( (0.7, 0.1) )
    
    n6.putWeights ( (0.1 ,) )
    n7.putWeights ( (0.2 ,) )
    
    # Insert the inputs
    n1.putInput (1.0)
    n2.putInput (2.0)
    n3.putInput (3.0)
    
    
    print colored ("Output value: %r", fg="yellow") % n8.getValue ()
    
