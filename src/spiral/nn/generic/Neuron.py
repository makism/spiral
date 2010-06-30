"""

"""


# batteries
import gobject
# spiral framework
from spiral.nn.generic import StepActivation
from spiral.nn.generic import SimpleMath
from spiral.nn.generic.synapse import Synapse
from spiral.helper import Pool
from spiral.nn import globals



class Neuron (gobject.GObject):
    """
    
    """
    
    __gsignals__ = {
        "activation"   : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )),
        "scatter-input": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )),
        "gather-inputs": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )),
        "flushed": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( ))
    }
    
    __gproperties__ = {
        "input": (
            gobject.TYPE_PYOBJECT, "The list with all inputs", None, gobject.PARAM_READWRITE
        ),
        "value": (
            gobject.TYPE_PYOBJECT, "The activation value", None, gobject.PARAM_READWRITE
        )
    }
    
    
    def __init__ (self, Id, LayerId, Name=None):
        """
        
        """
        gobject.GObject.__init__ (self)
        
        # Neuron identification number (unique in the layer).
        self.Id = Id
        
        # Layer`s id number (also unique).
        self.LayerId = LayerId
        
        # The number of inputs.
        self.numberOfInputs = 0
        
        # The list of synapses.
        self.synapses = dict ()
        
        # The total number of synapses.
        self.numberOfSynapses = 0
        
        # The current number of number of synapses.
        # that have "fired".
        self.numberOfSynapsesFired = 0
        
        # The total value of the neuron.
        self.value = 0.0
        
        # How many times has the output value has been read?
        self.valueAccessed = 0
        
        # Whether to emit notification signals.
        self.autoNotify = True
        
        # Whether to calculate the activation automatically
        # once all the inputs and weights have been gathered.
        self.autoActivation = True
        
        # Has the neuron been activated?
        self.hasActivated = False
        
        # The input, will be passed to each synapse.
        self.input = 0.0
        
                
        self.connect ("notify::input", self.neuronInputsUpdated)
        self.connect ("notify::value", self.neuronValueRead)
        
    def __str__ (self):
        base = self.__class__.__name__
        if self.hasActivated:
            return "[%s %d, Layer %d] Value: %r" % (base, self.Id, self.LayerId, self.value)
        else:
            return "[%s %d, Layer %d]" % (base, self.Id, self.LayerId)
    
    ##
    ##  GObject methods
    ##
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
        
    def do_activation (self):
        self.hasActivated = True
        
        for record in self.synapses.values ():
            for synapse in record.values ():
                synapse.putInput (self.get_property ("value"))
        
        self.numberOfSynapsesFired = 0
    
    ##
    ## Other methods
    ## 
    def getValue (self):
        #if self.hasActivated:
        return self.get_property ("value")            
        
    def setAutoNotify (self, Flag):
        self.autoNotify = Flag
        
    def setAutoActivation (self, Flag):
        self.autoActivation = Flag
        
    def createSynapse (self, Layer, Neuron):
        layer_id = None
        neuron_id= Neuron.Id
        
        # The layer id
        if isinstance (Layer, int):
            layer_id = Layer
        else:
            layer_id = Layer._Id
            
        if layer_id not in self.synapses.keys ():
            self.synapses [layer_id] = dict ()
                
        s = Synapse (self)
        s.connect ("input-updated", Neuron.synapseInputUpdated)
        s.connect ("weight-updated", Neuron.synapseWeightsUpdated)
        s.connect ("notify-src-connect", self.synapseConnectionEstablised)
        s.connect ("notify-target-connect", Neuron.synapseAddedAsTarget)
        s.connect ("notify-target-disconnect", Neuron.synapseConnectionDestroyed)
        s.connect ("fire", Neuron.synapseFired)
        s.connectTo (Layer, Neuron)
        
        if neuron_id not in self.synapses [layer_id].keys ():
            self.synapses [layer_id][neuron_id] = s
            
        self.numberOfSynapses += 1
        
    def destroySynapse (self, Layer, targetNeuron):
        layer_id = None
        neuron_id= None
        
        # is target neuron an object?
        if isinstance (targetNeuron, Neuron):
            neuron_id = targetNeuron.Id
        
        # or an integer?
        else:
            neuron_id = targetNeuron
            
        # The layer id
        if isinstance (Layer, int):
            layer_id = Layer
        else:
            layer_id = Layer._Id
        
        res = self.synapses [layer_id][neuron_id].disconnectFrom (self)
        del self.synapses [layer_id][neuron_id]
        
        self.numberOfSynapses -= 1
        
    def putInput (self, Input):
        self.input = Input
        
        if self.autoNotify:
            self.notify ("input")
            
    def putWeights (self, Weights):
        if len(Weights) == self.numberOfSynapses:
            
            i = 0
            for layer_id in self.synapses:
                allSynapses = self.synapses [layer_id]
                
                for synapse in allSynapses.values ():
                    synapse.putWeight (Weights[i])
                    
                    i += 1
                    
    def flush (self, value=True, input=True, synapses=True):
        # Reset the value
        if value:
            self.set_property ("value", 0.0)
        
        # Reset the input
        if input:
            self.set_property ("input", 0.0)
        
        # Reset the input of the synapses
        if synapses:
            for layer_id in self.synapses:
                allsynapses = self.synapses [layer_id]
            
                for neuron, synapse in allsynapses.iteritems():
                    synapse.flush ()
        
        # Reset the number of the synapses that have fired!
        self.numberOfSynapsesFired = 0
        
        self.emit ("flushed")
        
    def getSynapses (self):
        return self.synapses
    
    def getSynapseByLayer (self, LayerId):
        if LayerId in self.synapses.keys ():
            return self.synapses [LayerId]
        else:
            return None
        
    def getNumberOfIncomingSynapses (self):
        return self.numberOfInputs
    
    def getNumberOfSynapses (self):
        return self.numberOfSynapses
        
    def searchInSynapases (self, LayerId, NeuronId):
        if LayerId in self.synapses.keys ():
            if NeuronId in self.synapses [LayerId].keys ():
                return self.synapses [LayerId] [NeuronId]
    
    ##
    ##  Neuron-related signals
    ##
    def neuronValueRead (self, object, property):
        self.valueAccessed += 1
        
    def neuronInputsUpdated (self, object, property):
        if globals.runInDebug:
            print "[Neuron %d, Layer %d] Inputs have changed! Notifying all synapses." % \
                    (self.Id, self.LayerId)
        
        # Forward the input to the synapses
        for record in self.synapses.values ():
            for synapse in record.values ():
                synapse.putInput (self.input)
    
    ##
    ##  Synapse-related signals
    ##
    def synapseFired (self, Synapse):
        self.numberOfSynapsesFired += 1
        
        if self.numberOfSynapsesFired <= self.numberOfInputs:
            prev = self.get_property ("value")
            self.set_property ("value", prev + Synapse.getValue ())
        
        # When _all_ incoming synapses have fired, activate the neuron!
        if self.numberOfSynapsesFired == self.numberOfInputs:
            val = StepActivation.sigmoid (self.get_property ("value"))
            self.set_property ("value", val)
            
            self.emit ("activation")
    
    def synapseWeightsUpdated (self, object, property):
        if globals.runInDebug:
            print "[Neuron %d, Layer %d] Weight change, new value: %r." % \
                    (object.source.Id, object.source.LayerId, property)
            print "[Neuron %d, Layer %d] Notifying Neuron %d at Layer %d." % \
                    (object.source.Id, object.source.LayerId, object.target.Id, object.target.LayerId)
    
    def synapseInputUpdated (self, object, property):
        if globals.runInDebug:
            print "[Neuron %d, Layer %d] Input change, new value: %r." % \
                    (object.source.Id, object.source.LayerId, property)
            print "[Neuron %d, Layer %d] Notifying Neuron %d at Layer %d." % \
                    (object.source.Id, object.source.LayerId, object.target.Id, object.target.LayerId)
        
    def synapseAddedAsTarget (self, Synapse, targetNeuron, sourceNeuron):
        self.numberOfInputs += 1
        
        if globals.runInDebug:
            print "[Neuron %d, Layer %d] Neuron %d at Layer %d, connected with me." % \
                    (sourceNeuron.Id, sourceNeuron.LayerId, targetNeuron.Id, targetNeuron.LayerId)
            
    def synapseRemovedAsTarget (self, Synapse, targetNeuron, sourceNeuron):
        self.numberOfInputs -= 1
        
        if globals.runInDebug:
            print "[Neuron %d, Layer %d] Neuron %d at Layer %d disconnected from me." % \
                    (sourceNeuron.Id, sourceNeuron.LayerId, targetNeuron.Id, targetNeuron.LayerId)
            
    def synapseConnectionDestroyed (self, Synapse, Neuron):
        if globals.runInDebug:
            print "[Neuron %d, Layer %d] Disconnected from Neuron %d at Layer %d." % \
                    (self.Id, self.LayerId, Neuron.Id, Neuron.LayerId)
    
    def synapseConnectionEstablised (self, Synapse):        
        if globals.runInDebug:
            print "[Neuron %d, Layer %d] Connected with Neuron %d at Layer %d." % \
                    (self.Id, self.LayerId, Synapse.target.Id, Synapse.target.LayerId)
    

gobject.type_register (Neuron)
