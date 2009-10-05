"""

"""


# batteries
import gobject



class Registry (gobject.GObject):
    
    __instances__ = dict ()
    
    def __init__ (self, Name):
        gobject.GObject.__init__ (self)
        
        # Registry`s name.
        self._Name = Name
    
    @classmethod
    def getRegistry (cls, Name):
        if Name not in Registry.__instances__.keys ():
            Registry.__instances__ [Name] = Registry (Name)
        
        return Registry.__instances__ [Name]
    
