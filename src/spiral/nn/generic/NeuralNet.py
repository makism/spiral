"""

"""


# batteries
import gobject
import time
# spiral framework
from spiral.nn.generic import Neuron
from spiral.nn.generic.layer import NeuronLayer
from spiral.helper.Pool import ListPool



class NeuralNet (gobject.GObject, ListPool):
    """
    
    """
    
    __gsignals__ = {
        "weights-inserted": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )),
        "inputs-inserted" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( ))
    }
    
    __gproperties__ = {
        
    }
    
    
    def __init__ (self, Inputs, Outputs, Layers=None, NeuronsPerLayer=None, Name=""):
        gobject.GObject.__init__ (self)
        ListPool.__init__ (self)
        
        # Name
        self.Name = Name
        
        # Are our layers symmetric?
        if Layers is not None and NeuronsPerLayer is not None:
            self.SymmetricLayers = True
        else:
            self.SymmetricLayers = False
            
        # The number of inputs
        self.NumberOfInputs = Inputs
        
        # The number of outputs (the Neurons).
        self.NumberOfOutputs= Outputs
        
        # The number of layers, excluding the Input and Ouput.
        self.NumberOfLayers = Layers
        
        # The number of neurons that each layer will have.
        self.NumberOfNeuronsPerLayer = NeuronsPerLayer
        
        # Input/Output/Hidden layers.
        # Input layer is always at index 0.
        # Output layes is always at the end of the list.
        self.Layers = list ()
        self._pool = self.Layers
        
        # Some flags
        self.NetworkCreated = False
        
        # All weights
        self.Weights = None
        
        # All inputs
        self.Inputs = None
        
        # Output values
        self.Output = list ()
        
        # Total number of weights
        self.NumberOfWeights = 0
        
        # Does this network has an extra bias layer attached
        # to each hidden layer?
        self.HasBiasLayer = False
        
        # Store times for different methods. Used for benchmarking.
        self.keepTime = dict ()
        
    def __str__ (self):
        base = self.__class__.__name__
        if self.Name != "":
            return "%s Neural Network \"%s\", with %d hidden layer(s)." % (base, self.Name, self.NumberOfLayers)
        else:
            return "%s Neural Network, with %d hidden layer(s)." % (base, self.NumberOfLayers)
    
    """
        Other methods
    """
    def getInfo (self):
        pass
    
    def createNet (self):
        pass
    
    def stateSave (self, filename):
        pass
    
    def stateRestore (self, filename):
        pass
    
    def _putInputs (self, Inputs):
        if len (Inputs) == self.NumberOfInputs:
            self.Inputs = Inputs
                        
            # put the inputs on each neuron
            for i in range (self.NumberOfInputs):
                input_neuron = self [0][i]
                input_neuron.putInput (self.Inputs[i])
                
            # update the inputs in the bias layers
            try:
                if self.HasBiasLayer:
                    for layer in self:
                        if layer.biasLayer is not None:
                            layer.biasLayer.putBiasInputs ()
            except Exception:
                        pass
    
    def _putWeights (self, Weights):
        self.Weights = Weights
        
        start= 0
        stop = 0
        layer_id = 0
        for layer in self:            
            # put weights on each neuron
            for neuron in layer:
                size = neuron.getNumberOfSynapses ()
                
                stop = start + size 
                
                slice = self.Weights [start:stop]
                
                neuron.putWeights (slice)
                
                start = stop
                
            # put weights on each bias layer
            try:
                if self.HasBiasLayer and layer_id > 0:
                    size = layer.getLayerSize ()
                    stop = start + size
                    slice= Weights [start:stop]
                    layer.putBiasWeights (slice)
                    start = stop
            except Exception:
                pass
                
            layer_id += 1
    
    def getWeights (self):
        return self.Weights
    
    def getTotalWeights (self):
        return len (self.Weights)
    
    def update (self, inputs=None, weights=None):
        start = time.clock ()
        
        if self.Inputs is not None and \
           self.Weights is not None:
            self.flush ()
        
        if weights is None:
            self._putWeights (self.Weights)
        else:
            self._putWeights (weights)
            
        if inputs is None:
            self._putInputs (self.Inputs)
        else:
            self._putInputs (inputs)
            
        self.Output = list ()
        
        for i in range (self.NumberOfOutputs):
            for neuron in self [self.NumberOfLayers+1]:
                self.Output.append (neuron.getValue())
        
        self.keepTime['update'] = time.clock () - start
    
    def flush (self):
        for layer in self:
            if self.HasBiasLayer:
                if layer.biasLayer is not None:
                    layer.biasLayer.flush ()
            
            for neuron in layer:
                neuron.flush ()
    
    def output (self, index=None):
        if index is not None:
            if index <= len (self.Output):
                return self.Output [index]
        else:
            return self.Output
    
    def addLayer (self, Layer):
        self.Layers.append (Layer)
    
    def addLayers (self, Layers):
        self.Layers.extend (Layers)
    
    def removeLayer (self, LayerId):
        pass
    
    def getLayer (self, index):
        return self [index]
    
    def getTotalInputs (self):
        return self.NumberOfInputs
    
    def getTotalOutputs (self):
        return self.NumberOfOutputs
    
    def getTotalLayers (self):
        return self.NumberOfLayers
    
    def createDefaultSynapses (self):
        pass
    
    def timeUpdate (self):
        return self.keepTime['update']
    
    """
        Signals
    """
    def layerCreated (self, Layer):
        self.NumberOfWeights += Layer.numberOfBiasWeights
        
    def layerConnected (self, Layer):
        self.NumberOfWeights += Layer.numberOfWeights
    
    def layerDisconnected (self, Layer):
        self.NumberOfWeights -= Layer.numberOfWeights
        self.NumberOfWeights -= Layer.numberOfBiasWeights
    
