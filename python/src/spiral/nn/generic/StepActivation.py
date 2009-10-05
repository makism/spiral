"""

"""


# batteries
import math



def sigmoid (Activation, p=1.0):
    num = (-Activation)/p
    return 1/(1+math.exp(num))


def hard_limiter (Activation, p=1.0):
    pass


def ramp (Activation, p=1.0):
    pass
