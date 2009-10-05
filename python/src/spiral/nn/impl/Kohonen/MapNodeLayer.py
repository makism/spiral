"""

"""


# battaries
import gobject
# spiral framework
from spiral.nn.generic.layer import NeuronLayer
from spiral.nn.impl.Kohonen import MapNode



class MapNodeLayer (NeuronLayer):
    """
    
    """
    
    def __init__ (self, Neurons, AddBias=False, Name=None):
        NeuronLayer.__init__ (self, Neurons, AddBias=False, Name=Name)
        
        # Remove uneeded member variables
        del self.biasLayer, self.numberOfBiasWeights
     
    ##
    ## Other methods
    ##
    def createLayer (self):
        if len (self) == 0:
            # Create the neurons
            id = self.numberOfNeurons-1
            for i in range (self.numberOfNeurons):
                self.neurons.append ( MapNode (
                        Id = id,
                        LayerId = self.Id,
                    )
                )
                
                id -= 1
                
            # Create the bias layer
            if self.hasBiasLayer:
                self.biasLayer.connect ("bias-layer-connected", self.biasLayerConnected)
                self.biasLayer.connectTo (self)
            
            self.emit ("layer-created")    
    
gobject.type_register (NeuronLayer)

