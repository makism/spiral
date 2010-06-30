"""

"""

# batteries
import gobject
# spiral framework
from spiral.nn import globals
from spiral.nn.generic import Neuron
from spiral.nn.generic.synapse import BidiSynapse
from spiral.nn.generic import StepActivation


class BidiNeuron (Neuron):
    """
    A neuron that supports both one-directional synapses as well as bidirectional synapses.
    """
    
    
    def __init__ (self, Id, LayerId, Name=None):
        Neuron.__init__ (self, Id, LayerId, Name)
        
        # Bidirectional Synapses
        self.inputBidiSynapses = dict ()
        self.outputBidiSynapses= dict ()
        
        # Total number of bidirectional synapses
        self.numberOfBidiSynapses = 0
        self.numberOfInputBidiSynapses = 0
        self.numberOfOutputBidiSynapses= 0
        
        # The current number of number of synapses.
        # that have "fired".
        self.numberOfBidiSynapsesFired      = 0
        self.numberOfInputBidiSynapsesFired = 0
        self.numberOfOutputBidiSynapsesFired= 0
        
        # The current bidi synapses that have
        # successfuly fired (an in "input"), so
        # that we release the lock ;)
        self.indexOfFiredBidiSynapses = list ()
    
    ##
    ##  GObject methods
    ##
    def do_activation (self):
        #if not self.hasActivated:
        #    self.hasActivated = True
            
        self.numberOfSynapsesFired = 0
        self.numberOfInputBidiSynapsesFired = 0
        self.numberOfOutputBidiSynapsesFired = 0
        
        for r in self.inputBidiSynapses.values ():
            for inputSynapse in r.values ():
                if inputSynapse.lockOwner is self:
                    inputSynapse.putInput (self.get_property ("value"))
                    #inputSynapse.releaseLock ()

        for r in self.outputBidiSynapses.values ():
            for outputSynapse in r.values ():
                if outputSynapse.lockOwner is self:
                    outputSynapse.putInput (self.get_property ("value"))
                    #outputSynapse.releaseLock ()
        
    ##
    ##  Other methods
    ##
    def propagate (self):
        if self.numberOfOutputBidiSynapses > 0:
            print "Forward propagating..."
    
    def backPropagate (self):
        if self.numberOfInputBidiSynapses > 0:
            print "Propagating backwords..."
    
    def createBidiSynapse (self, targetNeuron):
        """
        Create a connection with the target neuron, using a bidirection synapse.
        """
        self.outputBidiSynapses [targetNeuron.LayerId] = dict ()
        
        # Create the bidisynapse
        b = BidiSynapse (self)
        # Connect the signals with the source neuron.
        b.connect ("input-updated", self.bidiSynapseInputUpdated)
        b.connect ("weight-updated", self.bidiSynapseWeightsUpdated)
        b.connect ("lock-acquired", self.bidiSynapseLockAcquired)
        b.connect ("lock-released", self.bidiSynapseLockReleased)
        b.connect ("bifire", self.bidiSynapseFired)
        # Connect the signals with the target neuron, and then create the actual
        # connection.
        b.connect ("input-updated", targetNeuron.bidiSynapseInputUpdated)
        b.connect ("weight-updated", targetNeuron.bidiSynapseWeightsUpdated)
        b.connect ("bifire", targetNeuron.bidiSynapseFired)
        b.connect ("notify-endpoint-connect", targetNeuron.bidiSynapseNotifyEndpointConnect)
        b.connect ("lock-acquired", targetNeuron.bidiSynapseLockAcquired)
        b.connect ("lock-released", targetNeuron.bidiSynapseLockReleased)
        b.connectTo (targetNeuron)
        b.acquireLock (self)
        # Store the actual bidi synapse.
        self.outputBidiSynapses [targetNeuron.LayerId][targetNeuron.Id] = b
        
        self.numberOfOutputBidiSynapses += 1
        self.numberOfBidiSynapses += 1
        
        return b
                        
    def putWeights (self, Weights):
        """
        Put the weights on the output bidirection synapses, and then forward the rest
        of the weights to the "one-way" synapses.
        """
        totalWeightsNeeded = self.numberOfInputs+self.numberOfOutputBidiSynapses 
        if len(Weights) >= totalWeightsNeeded:
            i = 0
            
            # Put the needed weights to the bidi synapses.
            for layer_id in self.outputBidiSynapses:
                allSynapses = self.outputBidiSynapses [layer_id]
                
                for synapse in allSynapses.values ():
                    if synapse.lockOwner == self:
                        synapse.putWeight (Weights[i])
                    
                        i += 1
            
            # Put the reset of the weights to the normal synapses.
            if self.numberOfInputs > 0:
                restOfWeights = Weights[i:]
                self.putWeights (self, restOfWeights)
                        
    ##
    ## Neuron-related signals
    ##        
    def neuronInputsUpdated (self, object, property):
        """
        Pass the input value to all synapses except the input bidisynapses.
        """
        if self.numberOfSynapses > 0:
            Neuron.neuronInputsUpdated (self, object, property)
        
        for layer in self.outputBidiSynapses.values ():
            for neuron, bidisynapse in layer.iteritems ():
                bidisynapse.putInput (self.input)
         
        for layer in self.inputBidiSynapses.values ():
            for neuron, inputSynapse in layer.iteritems ():
                inputSynapse.putInput (self.input)
    
    ##
    ## Synapse-related signals
    ##
    def bidiSynapseNotifyEndpointConnect (self, BidiSynapse):
        """
        
        """
        BidiSynapse.endPoint = self
        
        layer_id = BidiSynapse.startPoint.LayerId
        neuron_id= BidiSynapse.startPoint.Id
        
        if layer_id not in self.inputBidiSynapses.keys ():
            self.inputBidiSynapses [layer_id] = dict ()
        
        if neuron_id not in self.inputBidiSynapses [layer_id]:
            self.inputBidiSynapses [layer_id][neuron_id] = BidiSynapse
        
            # keep track of the total number of the synapses
            self.numberOfInputBidiSynapses += 1
            self.numberOfSynapses += 1
            # update the number of inputs this neuron accepts
            self.numberOfInputs += 1
            
            BidiSynapse.emit ("notify-bidisynapse-connected")
        else:
            BidiSynapse.emit ("notify-bidisynapse-connection-failed")
    
    def bidiSynapseFired (self, BidiSynapse):
        lockOwner = BidiSynapse.lockOwner
        
        if lockOwner is self:
            self.numberOfOutputBidiSynapsesFired += 1
            BidiSynapse.releaseLock ()
            
        else:
            # Let`s find out to which neuron/direction the firing
            # takes place :-)
            neuron = None
            if lockOwner is BidiSynapse.startPoint:
                neuron = BidiSynapse.endPoint
                numberOfWhatSynapses = self.numberOfInputBidiSynapses
                numberOfWhatSynapsesFired = self.numberOfInputBidiSynapsesFired
                #neuron.numberOfInputBidiSynapsesFired += 1
            else:
                neuron = lockOwner
                numberOfWhatSynapses = self.numberOfOutputBidiSynapses
                numberOfWhatSynapsesFired = self.numberOfOutputBidiSynapsesFired
                #neuron.numberOfOutputBidiSynapsesFired += 1
            
            BidiSynapse.acquireLock (self)                
            self.numberOfSynapsesFired +=1
            
            if numberOfWhatSynapsesFired <= 1:
                prev = self.get_property ("value")
                self.set_property ("value", prev + BidiSynapse.getValue ())
            
            # Activate the neuron if all the input synapses have fired!
            if numberOfWhatSynapsesFired == numberOfWhatSynapses:
                val = StepActivation.sigmoid (self.get_property ("value"))
                self.set_property ("value", val)
                
                self.emit ("activation")
    
    def bidiSynapseInputUpdated (self, BidiSynapse, InputValue):
        if globals.runInDebug:
            source = BidiSynapse.lockOwner
            if source is not self:
                print "[Neuron %d, Layer %d] Input change, new value: %r." % \
                        (source.Id, source.LayerId, InputValue)
                print "[Neuron %d, Layer %d] Notifying Neuron %d at Layer %d." % \
                        (source.Id, source.LayerId, self.Id, self.LayerId)
            else:
                print "(notifying self event, ignored)"
    
    def bidiSynapseWeightsUpdated (self, *args):
        pass
    
    def bidiSynapseLockReleased (self, BidiSynapse):
        if BidiSynapse.lockOwner is not self:
            print "[Lock Released] by %s" % BidiSynapse.lockOwner
            BidiSynapse.acquireLock (self)
    
    def bidiSynapseLockAcquired (self, BidiSynapse):
        if BidiSynapse.lockOwner is not self:
            print "[Lock Acquired] by %s" % BidiSynapse.lockOwner
    

gobject.type_register (BidiNeuron)
