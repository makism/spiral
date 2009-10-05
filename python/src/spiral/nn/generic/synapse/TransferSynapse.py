"""

"""


# batteries
import gobject



class TransferSynapse (gobject.GObject):
    
    
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
        "input-updated" : (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )
        ),
        "fire": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        )
    }
    
    __gproperties__ = {
        "input":  (gobject.TYPE_PYOBJECT,
                   "the synapse`s input", "",
                   gobject.PARAM_READWRITE
        )
    }
    
    
    def __init__ (self, source):
        gobject.GObject.__init__ (self)
        
        # The source neuron
        self.source = source
        
        # The target neuron
        self.target = None
        
        # Input
        self.input = input
        
        # Value
        self.value = 0.0
        
        self.connect ("notify::input",  self.emitInputUpdated)
    
    ##
    ##  Other methods
    ##
    def putInput (self, input):
        self.set_property ("input", input)
        
        if not self.frozen:
            self.emit ("sum")    
    def connectTo (self, Layer, Neuron):
        self.layer  = Layer
        self.target = Neuron
        self.emit ("notify-src-connect")
        self.emit ("notify-target-connect", self.source, Neuron)
        
    def disconnectFrom (self, Neuron):
        self.emit ("notify-target-disconnect", self.source)
        
    def getValue (self):
        return self.get_property ("value")
      
    ##
    ##  Signal-emitting methods
    ##
    def emitInputUpdated (self, obj, prop):
        self.emit ("input-updated", self.input)
      
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
    

gobject.type_register (TransferSynapse)
