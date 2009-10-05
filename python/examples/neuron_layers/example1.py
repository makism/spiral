#!/usr/bin/env python
"""

"""


# batteries
import sys
sys.path.append ("../../src/")
# spiral framework
from spiral.nn import globals
from spiral.nn.generic.layer import NeuronLayer
from spiral.helper import colored

 

if __name__ == "__main__":
    globals.runInDebug = True
    
    input_layer  = NeuronLayer (Name="Input Layer"    , Neurons=3)
    input_layer.createLayer ()
    first_hidden = NeuronLayer (Name="Hidden Layer #1", Neurons=2, AddBias=True)
    first_hidden.createLayer ()
    second_hidden= NeuronLayer (Name="Hidden Layer #2", Neurons=2, AddBias=True)
    second_hidden.createLayer ()
    output_layer = NeuronLayer (Name="Output Layer"   , Neurons=1, AddBias=True)
    output_layer.createLayer ()
    
    print "*" * 100
    input_layer.connectTo (first_hidden)
    print "*" * 50
    first_hidden.connectTo (second_hidden)
    print "*" * 50
    second_hidden.connectTo (output_layer)
    print "*" * 50
    
    
    input_layer.putInputs   ( (1.0, 2.0, 3.0) )
    input_layer.putWeights  ( (0.3, 0.4, -0.11, -0.8, -0.25, 0.25) )
    
    first_hidden.putWeights ( (1.0, 0.8, 0.7, 0.1) )
    first_hidden.putBiasWeights ( (0.5, -0.5) )
    first_hidden.biasLayer.putBiasInputs ()
    
    second_hidden.putWeights( (0.1, 0.2) )
    second_hidden.putBiasWeights ( (0.5, -0.5) )
    second_hidden.biasLayer.putBiasInputs ()
    
    output_layer.putBiasWeights ( (0.5,) )
    output_layer.biasLayer.putBiasInputs ()

    print colored("Output: %r", fg="yellow") % output_layer [0].getValue ()
