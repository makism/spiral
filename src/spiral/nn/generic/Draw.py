""""

"""


# batteries
import cairo
# spiral framework
#from spiral.nn.impl import Feedforward



class Draw (object):
    
    def __init__ (self, NeuralNetwork, Size):
        
        if isinstance (NeuralNetwork, Feedforward):
            self.drawer = FeedforwardDrawer ()
            
        self._w, self._h = Size
        self._Surface = cairo.ImageSurface (cairo.FORMAT_RGB24, self._w, self._h)
        self._Context = cairo.Context (self._Surface)
        
        
        self._totalInputs  = NeuralNetwork.getTotalInputs ()
        self._totalOutputs = NeuralNetwork.getTotalOutputs ()
        self._totalLayers  = len (NeuralNetwork)
        self._maxLayerSize = 0
        
        
    def _createGrid (self):
        self._Context.set_source_rgb (1, 1, 1)
        self._Context.set_operator (cairo.OPERATOR_SOURCE)
        self._Context.paint ()
        
        self._Context.set_source_rgb (0.237, 0.237, 0.237)
        
        for i in range (self._w/25):
            self._Context.move_to (25+(i*25), 0 )
            self._Context.line_to (25+(i*25), self._w )
        
        for i in range (self._h/25):
            self._Context.move_to (0, 25+(i*25))
            self._Context.line_to (self._w, 25+(i*25))
        
        self._Context.set_line_width (0.1)
        self._Context.stroke ()
        
    def render (self):
        self._createGrid ()
        
        for i in range (self._totalInputs):
            self._Context.set_source_rgb (0.0, 0.0, 0.0)
            self._Context.select_font_face ("Georgia", cairo.FONT_SLANT_NORMAL)
            self._Context.set_font_size (12)
            self._Context.move_to (100, 50 + (i*50))
            self._Context.show_text ("i%d" % (i+1))
        
            self._Context.rectangle (95, 50 + (i*50)-13, 20, 20);
            self._Context.set_line_width (2);
            self._Context.set_line_join (cairo.LINE_JOIN_MITER); 
            self._Context.stroke ();
    
    def save (self, imagename):
        self._Surface.write_to_png (imagename)
    

class FeedforwardDrawer (object):
    
    def __init__ (self):
        pass