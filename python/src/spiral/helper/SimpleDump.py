# coding=UTF-8
"""

"""

# batteries
import types
import pprint
# spiral framework
from spiral.helper import colored, colored_value



def _simple_dump_init (Object, Name=None, FullExposure=False):
    """
    
    """
    header = ""
    what_type = `type (Object)`[8:]
    what_type = what_type[:len(what_type)-2]
    introspect= dir (Object)
    
    properties = dict ()
    inherited_properties = dict ()
    methods    = dict ()
    
    for m in introspect:
        if not FullExposure:
            if m.startswith ("__") and m.endswith ("__"):
                continue
        
        target = getattr (Object, m)
        if callable (target):
            methods [m] = str (target).__doc__
        else:
            t = `type (target)`[7:].strip("'>< ") 
            #t = t[:len(t)-2]
            properties[m] = {
                "type" : t,
                "value": target
            }
    
    # Define the header
    if Name is not None:
        header = "Dumping instance %s of class %s" % (colored(Name, fg="bold"), colored(what_type, fg="underline"))
    else:
        header = "Dumping instance of class %s" % (colored(what_type, fg="underline"))
    
    print header
    
    data = {
        "method": methods,
        "properties": properties
    }
    
    return data
    

def dump_properties (Object, watchProps=None, Name=None, FullExposure=False, showType=False, showVal=True, showTitle=False):
    """
    
    """
    data = _simple_dump_init (Object, Name, FullExposure)
    
    if watchProps is not None:
        title = "Watching Properties"
        props = dict ()
        
        for p in watchProps:
            if p in data['properties']:
                props [p] = data['properties'][p]
    else:
        title = "Properties"
        props = data['properties']
    
    total = len (props)
    
    if total > 0:
        if showTitle: print "%s (%d):\n│" % (title, total)
        
        # Make the output pretty :-)
        spacing_name = 0
        spacing_type = 0
        for p in props.iterkeys():
            prop_name_len = 0
            
            if FullExposure:
                prop_name_len = len (p)
            else:
                if not p.startswith ("__") and not p.endswith ("__"):
                    prop_name_len = len (p)
            
            if prop_name_len > spacing_name: spacing_name = prop_name_len
            
            prop_type_len = len (props[p]['type'])
            if prop_type_len > spacing_type: spacing_type = prop_type_len
        
        # Print the properties order by name.
        counter = 0
        bgcolor = None
        s = sorted(props.iterkeys())
        for p in s:
            
            prop_name = p.ljust (spacing_name)
            prop_type = props[p]['type'].ljust (spacing_type)
            prop_val  = props[p]['value']
            
            if counter < total-1:
                symbol = "├─"
            else:
                symbol = "└─"
            
            """
            if p == "__gdoc__" or p == "__doc__":
                print "`--", colored(prop_name, fg="bold"), ":", prop_type, ":", prop_val                    
                continue                    
            """
            
            print symbol, colored(prop_name, fg="bold"),
            
            if showType: print ":", prop_type,
            if showVal:
                if type (prop_val) is types.DictionaryType or \
                    type (prop_val) is types.ListType:
                    print ":",
                    pprint.pprint (prop_val)
                else:
                    print ":", colored_value (prop_val)
            if not showType and not showVal: print
            
            counter += 1
    
    print
    

def dump_methods (Object, Name=None):
    pass
    

def dump (val):
    t = `type (val)`[7:].strip("'>< ")
    
    print "(%s)" % t,
    if type (val) is types.DictionaryType or \
        type (val) is types.ListType:
        pprint.pprint (prop_val)
    else:
        print colored_value (val)
    
