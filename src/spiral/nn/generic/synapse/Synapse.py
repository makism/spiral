"""

"""

# battaries
import gobject
# spiral framework
from spiral.nn import globals
from spiral.helper import colored



class Synapse (gobject.GObject):
    """
    A one-way synapse.
    """
    
    __gsignals__ = {
        "notify-src-connect": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        ),
        "notify-src-disconnect": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )
        ),
        "notify-target-connect": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT)
        ),
        "notify-target-disconnect": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )
        ),
        "weight-updated" : (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )
        ),
        "input-updated" : (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )
        ),
        "fire": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        ),
        "sum": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        )
    }
    
    __gproperties__ = {
        "weight": (gobject.TYPE_PYOBJECT,
                   "the synapse`s weight", "",
                   gobject.PARAM_READWRITE
        ),
        "input":  (gobject.TYPE_PYOBJECT,
                   "the synapse`s input", "",
                   gobject.PARAM_READWRITE
        ),
        "value":  (gobject.TYPE_PYOBJECT,
                   "the actual value", "",
                   gobject.PARAM_READWRITE
        )
    }
    
    
    def __init__ (self, source=None, input=None, weight=None):
        gobject.GObject.__init__ (self)
        
        # The source neuron
        self.source = source
        
        # The target neuron
        self.target = None
        
        # Input
        self.input = input
        
        # The actual weight
        self.weight = weight
        
        # Target`s layer
        self.layer = None
        
        # Value
        self.value = 0.0
        
        # 'Has fired?' flag
        self.frozen = False
        
        self.connect ("notify::input",  self.emitInputUpdated)
        self.connect ("notify::weight", self.emitWeightsUpdated)
        
    ##
    ##  Other methods
    ##
    def putInput (self, input):
        self.set_property ("input", input)
        
        if not self.frozen:
            self.emit ("sum")
        
    def putWeight (self, weight):
        self.set_property ("weight", weight)
        
        if not self.frozen:
            self.emit ("sum")
            
    def connectTo (self, Layer, Neuron):
        self.layer  = Layer
        self.target = Neuron
        self.emit ("notify-src-connect")
        self.emit ("notify-target-connect", self.source, Neuron)
        
    def disconnectFrom (self, Neuron):
        self.emit ("notify-target-disconnect", self.source)
        
    def freeze (self):
        self.frozen = True
    
    def unfreeze (self):
        self.frozen = False
        
    def getValue (self):
        return self.get_property ("value")
    
    def flush (self, input=True, weight=True, value=True, state=True):
        if state:
            self.frozen = False
        
        if input:
            self.set_property ("input", None)
        
        if weight:
            self.set_property ("weight", None)
        
        if value:
            self.set_property ("value", None)
            
    ##
    ##  Signal-emitting methods
    ##
    def emitInputUpdated (self, obj, prop):
        self.emit ("input-updated", self.input)
        
    def emitWeightsUpdated (self, obj, prop):
        self.emit ("weight-updated", self.weight)
    
    ##
    ##  GObject methods
    ##
    def do_get_property (self, property):
        name = property.name
        
        if name in self.__dict__.keys ():
            return self.__dict__ [name]
        else:
            raise AttributeError, "No such attribute"
        
    def do_set_property (self, property, value):
        name = property.name
        
        if name in self.__dict__.keys ():
            self.__dict__ [name] = value
        else:
            raise AttributeError, "Not such attribute"
        
    def do_sum (self):
        if self.input is not None and self.weight is not None:
            self.set_property (
                "value", 
                self.get_property ("input") * self.get_property ("weight")
            )
            
            self.emit ("fire")
            
            if globals.runInDebug:
                print colored ("Synapse from Neuron %d at Layer %d fires to Neuron %d at Layer %d." % \
                        (self.source.Id, self.source.LayerId, self.target.Id, self.target.LayerId), "green")
    

gobject.type_register (Synapse)
