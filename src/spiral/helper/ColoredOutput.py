"""

"""


# batteries
import sys
import types



allcolors = {
    "default"    :     "\033[m",
    # styles
    "bold"       :     "\033[1m",
    "underline"  :     "\033[4m",
    "blink"      :     "\033[5m",
    "reverse"    :     "\033[7m",
    "concealed"  :     "\033[8m",
    # font colors
    "black"      :     "\033[30m", 
    "red"        :     "\033[31m",
    "green"      :     "\033[32m",
    "yellow"     :     "\033[33m",
    "blue"       :     "\033[34m",
    "magenta"    :     "\033[35m",
    "cyan"       :     "\033[36m",
    "white"      :     "\033[37m",
    # background colors
    "on_black"   :     "\033[40m", 
    "on_red"     :     "\033[41m",
    "on_green"   :     "\033[42m",
    "on_yellow"  :     "\033[43m",
    "on_blue"    :     "\033[44m",
    "on_magenta" :     "\033[45m",
    "on_cyan"    :     "\033[46m",
    "on_white"   :     "\033[47m" 
}


def colored (str, fg=None, bg=None, style=None):
    if sys.platform == "linux2":
        rstr = ""
        
        args = (fg, bg, style)
        for arg in args:
            if arg in allcolors.keys ():
                rstr += allcolors [arg]
                
        rstr += str + allcolors ['default']
        
        return rstr
    else:
        return str
    

def colored_value (value):
    t     = type (value)
    color = None
    
    if t is types.BooleanType:
        if value:
            color = "green"
        else:
            color = "red"
    elif t is types.IntType or t is types.LongType or t is types.FloatType:
        color = "yellow"
    
    return colored (`value`, fg=color)
