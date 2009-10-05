"""
    Ready to use logging facility. Great stuff :P
"""


import logging



l = logging.getLogger ()
l.setLevel(logging.DEBUG)

__fh = logging.FileHandler("debug.log")
__ch = logging.StreamHandler()
__fmt= logging.Formatter ("%(module)s.%(funcName)s :: %(message)s", "%H:%M:%S")

__fh.setLevel(logging.DEBUG)
__ch.setLevel(logging.ERROR)

__ch.setFormatter(__fmt)
__fh.setFormatter(__fmt)

l.addHandler (__ch)
l.addHandler (__fh)
