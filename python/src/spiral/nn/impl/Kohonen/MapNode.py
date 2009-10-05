"""

"""


# batteries
import gobject
# spiral framework
from spiral.nn import globals
from spiral.nn.generic import Neuron



class MapNode (Neuron):
    
    def __init__ (self, Id, LayerId):
        Neuron.__init__ (self, Id, LayerId)
        
        # Input value
        self.input = None
        
        # The associated feature map.
        self.featureMap = list ()
        
        # The number of inputs also define the length of the feature map. 
        self.numberOfInputs = 0
        
    ##
    ##  Synapse-related signals
    ##
    def synapseFired (self, Synapse):
        pass
    
    def synapseWeightsUpdated (self, object, property):
        pass
    
    def synapseInputUpdated (self, object, property):
        pass
    
    def synapseAddedAsTarget (self, Synapse, targetNeuron, sourceNeuron):
        self.numberOfInputs += 1
        
        if globals.runInDebug:
            print "[MapNode at (%d, %d)] MapNode at (%d, %d) connected with me." % \
                    (sourceNeuron.Id, sourceNeuron.LayerId, targetNeuron.Id, targetNeuron.LayerId)
    
    def synapseConnectionDestroyed (self, Synapse, Neuron):
        pass
    
    def synapseConnectionEstablised (self, Synapse):        
        if globals.runInDebug:
            print "[MapNode at (%d, %d)] Connected with MapNode at (%d, %d)." % \
                    (self.LayerId, self.Id, Synapse.target.LayerId, Synapse.target.Id)
    
    
gobject.type_register (MapNode)

