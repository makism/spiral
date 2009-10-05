"""

"""


# battaries
import gobject
# spiral framework
from spiral.nn.generic.layer import Layer
from spiral.nn.generic.layer import BiasLayer
from spiral.nn.generic import Neuron
from spiral.helper import Pool



class NeuronLayer (Layer):
    """
    
    """
    
    def __init__ (self, Neurons, AddBias=False, Name=None):
        Layer.__init__ (self, Neurons, AddBias, Name)
        
        # Has a bias layer?
        if AddBias:
            self.hasBiasLayer = True
        else:
            self.hasBiasLayer = False
        
        # Bias layer
        if self.hasBiasLayer:
            self.biasLayer = BiasLayer (self.numberOfNeurons)
        else:
            self.biasLayer = None
    
    """
        Other methods
    """
    def createLayer (self):
        if len (self) == 0:
            # Create the neurons
            for i in range (self.numberOfNeurons):
                self.neurons.append ( Neuron (
                        Id = i,
                        LayerId = self.Id,
                    )
                )
                
            # Create the bias layer
            if self.hasBiasLayer:
                self.biasLayer.connect ("bias-layer-connected", self.biasLayerConnected)
                self.biasLayer.connectTo (self)
            
            self.emit ("layer-created")
                
    def putBiasWeights (self, Weights):
        if self.hasBiasLayer:
            idx = 0
            for neuron in self.biasLayer:
                all_synapses = neuron.getSynapses ()
                
                for layer_id in all_synapses:
                    synapses = all_synapses [layer_id]
                    
                    for synapse_id in all_synapses [layer_id]:
                        target_synapse = synapses [synapse_id]
                        target_synapse.putWeight (Weights[idx])
                
                        idx +=1
        else:
            return

gobject.type_register (NeuronLayer)

