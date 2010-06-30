"""

"""


# batteries
import gobject
# spiral framework
from spiral.nn.generic import NeuralNet
from spiral.nn.impl.Kohonen import Kohonen 


class Kohonen2D (Kohonen):
    
    def __init__ (self, Inputs, Width, Height, Iterations=0, Name=""):
        Kohonen.__init__ (self, Inputs, Width, Height, Iterations, Name)
    

gobject.type_register (Kohonen2D)
    