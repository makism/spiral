#!/usr/bin/env python
"""

"""


# batteries
import sys
sys.path.append ("../../src/")
# spiral framework
from spiral.helper import colored
from spiral.nn import globals
from spiral.nn.generic import NeuralNet
from spiral.nn.generic.layer import NeuronLayer



class MyNetwork (NeuralNet):
    """ A simple neural network. Out input layer has only one neuron as well as
        the output layer. We also define two hidden layer containing two neuron
        each. """
    
    def __init__ (self, Inputs, Outputs, Layers=None, NeuronsPerLayer=None, Name=""):
        """ Pass the arguments to the parent class. """
        NeuralNet.__init__ (self, Inputs, Outputs, Layers, NeuronsPerLayer, Name)
    
    def createNet (self):
        """ Create the neurons, the layers and the synapses. """
        
        if not self.NetworkCreated:
            # Create input layer
            input_layer = NeuronLayer (Neurons = self.NumberOfInputs)
            input_layer.createLayer ()
            
            # Create the hidden layers
            hidden_layers = list ()
            for i in range (self.NumberOfLayers):
                hidden_layer = NeuronLayer (Neurons = self.NumberOfNeuronsPerLayer)
                hidden_layer.createLayer ()
                hidden_layers.append (hidden_layer)
            
            # Create the output layer
            output_layer = NeuronLayer (Neurons = self.NumberOfOutputs)
            output_layer.createLayer ()
            
            # Now, we must explicity declare the synapses!
            # We connect all neurons from input layer to the first hidden layer,
            # also we connect the input neuron to the output neuron! 
            input_layer.connectTo (hidden_layers[0])
            input_layer.connectTo (output_layer)
            
            # We connect the neurons of the first hidden layer wih the neurons
            # of the second hidden layer.
            # Also, we connect the second neuron of this layer (the first hidden)
            # to the neuron of the output layer.
            hidden_layers[0].connectTo (hidden_layers[1])
            hidden_layers[0][1].createSynapse (output_layer.Id, output_layer[0])
            
            # We connect the neurons of the second hidden layer to the output.
            hidden_layers[1].connectTo (output_layer)
            
            
            self.addLayers ( (input_layer, hidden_layers[0], hidden_layers[1], output_layer) )
            
            self.NetworkCreated = True


if __name__ == "__main__":
    # Change to `True`, to see what really happens...
    globals.runInDebug = False
    
    settings = {
        "Name"   : "Test Net",
        "Inputs" : 1,
        "Outputs": 1,
        "Layers" : 2,
        "NeuronsPerLayer": 2
    }
    
    nn = MyNetwork (**settings)
    nn.createNet ()
    
    inputs = [ 1.0 ]
    weights= [-0.80,  1.0,  0.25, \
               0.13, -0.47, 0.64, 0.99, 0.20, \
               -1.0,  0.72 ]
    
    
    print "Neural Network Settings:"
    print "     Input: 1.0"
    print "   Weights: -0.80, 1.0, 0.25, 0.13, -0.47, 0.64, 0.99, 0.20, -1.0, 0.72\n"
    
    raw_input("\nPress any key for the first run...") 
    
    nn.update (inputs, weights)
    print "Neural network output:", colored ("%r", fg="yellow") % nn.output ()[0]
    print
    print
    
    print "We keep the the starting weights, but we input the value: 0.5"
    raw_input("\nPress any key for the second run...")
    nn.update ( inputs=[0.5] )
    print "Neural network output:", colored ("%r", fg="yellow") % nn.output ()[0]
    print
    print
    
    print "We keep the the starting weights, but we input the value: -0.25"
    raw_input("\nPress any key for the second run...")
    nn.update ( inputs=[-0.25] )
    print "Neural network output:", colored ("%r", fg="yellow") % nn.output ()[0]
    print
    print
    
