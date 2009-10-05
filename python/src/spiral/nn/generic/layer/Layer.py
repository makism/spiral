"""

"""


import gobject
# spiral framework
from spiral.helper.Pool import ListPool  


class Layer (gobject.GObject, ListPool):
        
    __id = -1
    
    __gsignals__ = {
        "layer-created": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        ),
        "layer-connected": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        ),
        "layer-disconnected": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        )
    }
    
    __gproperties__ = {
        "Neurons":  (
            gobject.TYPE_PYOBJECT,
            "The list with all the neurons",
            "",
            gobject.PARAM_READWRITE
        )
    }
    
    
    def __init__ (self, Neurons, AddBias=False, Name=None):
        gobject.GObject.__init__ (self)
        ListPool.__init__ (self)
        
        # Unique id
        self.Id = Layer.__nextId ()
        
        # Name
        self.Name = Name
        
        # The total number of neurons 
        self.numberOfNeurons = Neurons
        
        # The list of neurons
        self.neurons = list ()
        self._pool = self.neurons
        
        #
        self.hasBiasLayer = False
        
        # 
        self.biasLayer = None
        
        # Total Number of Weights
        self.numberOfWeights = 0
        
        # Total Number Of Bias Weights
        self.numberOfBiasWeights = 0
        
        
    def __str__ (self):
        name = self.__class__.__name__
        return "%s #%d (%d neurons)" % (name, self.Id, self.numberOfNeurons)
        
    @classmethod
    def __nextId (cls):
        cls.__id += 1
        return cls.__id
    
    
    """
        GObject methods
    """
    def do_get_property (self, property):
        name = property.name
        
        if name in self.__dict__.keys ():
            return self.__dict__ [name]
        else:
            raise AttributeError, "Attribute \"%s\" does not exist." % name
    
    def do_set_property (self, property, value):
        name = property.name
        
        if name in self.__dict__.keys ():
            self.__dict__ [name] = value
        else:
            raise AttributeError, "Attribute \"%s\" does not exist." % name
    
    
    """
        Other methods
    """
    def addNeuron (self, Neuron):
        if len(self) != self.numberOfNeurons:
            self.neurons.append (Neuron)
        
    def getNeurons (self):
        return self.get_property ("Neurons")
            
    def connectTo (self, otherLayer):
        for neuron in self:
            for target_neuron in otherLayer:
                neuron.createSynapse (otherLayer.Id, target_neuron )
                
                self.numberOfWeights += 1
        
        self.emit ("layer-connected")
    
    def disconnectFrom (self, otherLayer):
        self.emit ("layer-disconnected")
    
    def putWeights (self, Weights):
        idx = 0
        for neuron in self:
            all_synapses = neuron.getSynapses ()
            
            for layer_id in all_synapses.keys ():
                synapses = all_synapses [layer_id]
                
                for synapse_id in synapses:
                    target_synapse = synapses [synapse_id]
                    target_synapse.putWeight (Weights[idx])
                    
                    idx += 1

    def putBiasInputs (self):
        pass
        
    def putBiasWeights (self, Weights):
        pass
    
    def putInputs (self, Inputs):
        for i in range (len (Inputs)):
            neuron  = self [i]
            neuron.putInput (Inputs[i])
    
    def getLayerSize (self):
        return self.numberOfNeurons
    
    """
        Layer-related signals
    """
    
    """
        Bias-related signals
    """
    def biasLayerConnected (self, BiasLayer):
        self.numberOfBiasWeights += BiasLayer.numberOfWeights    
    
