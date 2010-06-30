"""

"""


# batteries
import gobject
# spiral framework
from spiral.nn.generic.layer import Layer
from spiral.nn.generic import Neuron



class BiasLayer (Layer):
    
    __gsignals__ = {
        "bias-layer-created": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        ),
        "bias-layer-connected": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        )
    }
    
    
    def __init__ (self, Neurons):
        Layer.__init__ (self, Neurons, False, None)
        
        # Total number of neurons
        self.numberOfNeurons = Neurons
        
        # Default value
        self.bias = 1.0
        
    def __str__ (self):
        return "Bias Layer (%d neurons)" % self.numberOfNeurons
    
    """
        Other methods
    """
    def connectTo (self, otherLayer):
        for i in range (otherLayer.getLayerSize ()):
            neuron = otherLayer [i]
            BiasNeuron = Neuron (i, self.Id)
            BiasNeuron.createSynapse (otherLayer.Id, neuron)
            
            self.neurons.append (BiasNeuron)
            
            self.numberOfWeights += 1
         
        self.emit ("bias-layer-connected")
        
    def flush (self):
        for neuron in self.neurons:
            neuron.flush ()
        
    def disconnectFrom (self, otherLayer):
        pass
            
    def putBiasInputs (self):
        for neuron in self:
            neuron.putInput (self.bias)
    
    
gobject.type_register (BiasLayer)

