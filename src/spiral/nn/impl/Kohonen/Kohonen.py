"""

"""


# batteries
import gobject
# spiral framework
from spiral.nn.generic.synapse import TransferSynapse
from spiral.nn.generic import NeuralNet
from spiral.nn.impl.Kohonen import MapNodeLayer



class Kohonen (NeuralNet):
    
    def __init__ (self, Inputs, Width, Height, Iterations=1, Name=""):
        NeuralNet.__init__ (self, Inputs, Outputs=0, Layers=Width, NeuronsPerLayer=Height, Name=Name)
        
        # Remove uneeded member variables.
        del self.NumberOfOutputs, self.NumberOfNeuronsPerLayer, self.NumberOfLayers, self.HasBiasLayer
        
        #
        self.transferSynapses = dict ()
        tmp = TransferSynapse (self)
        
        #
        self.Map = None
        
        #
        self.Width = Width
        
        #
        self.Height= Height
        
        #
        self.inputLayer = None
        
        #
        self.totalIterations = Iterations
        
        #
        self.iteration = 1
    
    def __str__ (self):
        base = self.__class__.__name__
        if self.Name != "":
            return "%s Neural Network \"%s\", %dx%d." % (base, self.Name, self.Width, self.Height)
        else:
            return "%s Neural Network, %dx%d." % (base, self.Width, self.Height)
    
    ##
    ## Other methods
    ##
    def putInputs (self, Inputs):
        self._putInputs (Inputs)
    
    def putWeights (self, Weights):
        self._putWeights (Weights)
    
    def createNet (self):
        if not self.NetworkCreated:
            inputLayer = MapNodeLayer (Neurons = self.NumberOfInputs)
            inputLayer.createLayer ()
            self.Layers.append (inputLayer)
            
            for i in range (self.Width):
                new_layer = MapNodeLayer (Neurons=self.Height)
                new_layer.createLayer ()
                
                self.Layers.append (new_layer)
                
            self.NetworkCreated = True
    
    def createDefaultSynapses (self):
        """
        Connect all inputs with all mapnodes. Simple.
        """
        if self.NetworkCreated:
            for layer_id in range (1, self.Width+1):
                self.Layers[0].connectTo (self.Layers[layer_id])
    

gobject.type_register (Kohonen)
    
    