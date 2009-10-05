"""

"""



# spiral framework
from spiral.nn.generic import NeuralNet
from spiral.nn.generic.layer import NeuronLayer



class Feedforward (NeuralNet):
    
    def __init__ (self, Inputs, Outputs, Layers=None, NeuronsPerLayer=None, \
                   AddBias=False, StepActivation=None, Name=""):
        NeuralNet.__init__ (self, Inputs, Outputs, Layers, NeuronsPerLayer, Name)

        if AddBias:
            self.HasBiasLayer = True
        
        # Temporary layers
        self._TempLayers = list ()
    
    def createNet (self):
        if not self.NetworkCreated:
            # Create input layer.
            input_layer = self.addHiddenLayer (NumberOfNeurons = self.NumberOfInputs, AddToStack=False)
            
            # Create the hidden layers.
            if self.SymmetricLayers:
                for i in range (self.NumberOfLayers):
                    self.addHiddenLayer (
                        NumberOfNeurons = self.NumberOfNeuronsPerLayer,
                        AddBias = self.HasBiasLayer
                    )
            
            # Create the output layer.
            output_layer = self.addHiddenLayer (
                NumberOfNeurons = self.NumberOfOutputs,
                AddBias = self.HasBiasLayer,
                AddToStack=False
            )
            
            self.addLayer (input_layer)
            self.addLayers(self._TempLayers)
            self.addLayer (output_layer)
            
            self.NetworkCreated = True
            
    def addHiddenLayer (self, NumberOfNeurons, AddBias=False, AddToStack=True):
        if not self.NetworkCreated:
            new_layer = NeuronLayer (Neurons = NumberOfNeurons, AddBias = AddBias)
            new_layer.connect ("layer-created", self.layerCreated)
            new_layer.connect ("layer-connected", self.layerConnected)
            new_layer.connect ("layer-disconnected", self.layerDisconnected)
            new_layer.createLayer ()
            
            if AddToStack:
                self._TempLayers.append (new_layer)
            else:
                return new_layer
    
    def createDefaultSynapses (self):
        if self.NetworkCreated:
            # Connect the input layer with the next layer. The next layer can be 
            # the output layer if no hidden layers are specified.
            self [0].connectTo (self [1])
            
            # This is the case, when we have no hidden layers.
            if self.NumberOfLayers == 0:
                return
            
            # In the case we *have* hidden layers, we connect them all.
            else:
                for i in range (1, self.NumberOfLayers+1):
                    curr_layer = self [i]
                    
                    if i+1 <= self.NumberOfLayers+1:
                        next_layer = self [i+1]
                        curr_layer.connectTo (next_layer)
    
