#!/usr/bin/env python
"""

"""


# batteries
import sys
sys.path.append ("../../src/")
import gobject
# spiral framework
from spiral.nn import globals
from spiral.nn.generic import Neuron
from spiral.nn.generic import BidiNeuron
from spiral.nn.generic.synapse import BidiSynapse
from spiral.helper.SimpleDump import dump_properties, dump


    
if __name__ == "__main__":
    globals.runInDebug = True 
    
    n1 = BidiNeuron (Id=0, LayerId=0, Name="Input BidiNeuron")
    n2 = BidiNeuron (Id=0, LayerId=1, Name="Test BidiNeuron")
    
    bidi_synapse = n1.createBidiSynapse (n2)
    
    n1.putInput (1.0)    
    n1.putWeights ([0.5,])   
    
    print "*" * 143
    dump_properties (n1, watchProps=("input", "numberOfOutputBidiSynapsesFired", "numberOfInputBidiSynapsesFired", "value"), Name="n1")
    #dump_properties (n1, Name="n1")
    dump_properties (n2, watchProps=("input", "numberOfInputBidiSynapsesFired", "numberOfOutputBidiSynapsesFired", "value"), Name="n2")
    #dump_properties (n2, Name="n2")
    dump_properties (bidi_synapse, watchProps=("endPoint", "startPoint", "value", "input", "lockOwner"), Name="Bidi Synapse")
    print "*" * 143
    
    n1.propagate ()
    n2.backPropagate ()
    
    
