"""
    Bidirection-connected Synapse
"""


# batteries
import gobject
from threading import Lock
# spiral framework
from spiral.nn import globals
from spiral.helper import colored
from spiral.nn.generic.synapse import Synapse



class BidiSynapse (Synapse):
    """
    A bidirection synapse. This means that the same synapse can be used
    as input an output between two specific neurons.
    """
    
    __gsignals__ = {
        "notify-endpoint-connect": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )),
        "notify-bidisynapse-connected": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )),
        "otify-bidisynapse-connection-failed": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )),
        "bifire": (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )
        ),
        "lock-released": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( )),
        "lock-acquired": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ( ))
    }
    
    __gproperties__ = {
        "lockOwner": (gobject.TYPE_PYOBJECT,
                       "", "",
                       gobject.PARAM_READWRITE
        ),
    }
    
    
    def __init__ (self, source):
        Synapse.__init__ (self, source, None, None)
        
        # Remove some unused member variables.
        del self.source, self.layer, self.target
        
        # The lock owner ;). Who`s got the right to change the inputs.
        self.lockOwner = None
        
        # The starting point of the synapse.
        self.startPoint = source
        
        # The ending point of the synapse.
        self.endPoint = None
    
    ##
    ## Other methods
    ##
    def connectTo (self, Neuron):
        self.endPoint = Neuron
        self.emit ("notify-endpoint-connect")
        
    def acquireLock (self, newLocker):
        #if self.get_property ("lockOwner") is None:
            self.set_property ("lockOwner", newLocker)
            self.emit ("lock-acquired")
    
    def releaseLock (self):
        self.emit ("lock-released")
        self.set_property ("lockOwner", None)
        
    def freeze (self):
        self.frozen = True
    
    def unfreeze (self):
        self.frozen = False
    
    ##
    ## GObject methods
    ##
    def do_sum (self):
        if self.input is not None and self.weight is not None:
            self.set_property (
                "value", 
                self.get_property ("input") * self.get_property ("weight")
            )
            
            if globals.runInDebug:
                source = self.lockOwner
                target = None
                
                if source is self.startPoint:
                    target = self.endPoint
                else:
                    target = self.startPoint
                
                print colored ("BidiSynapse sums and fires\n\tFROM %s\n\tTO   %s", fg="green") % (source, target)
            
            self.emit ("bifire") 
    
    
gobject.type_register (BidiSynapse)
