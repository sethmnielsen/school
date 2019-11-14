import shared

if shared.USE_CUPY:
    import cupy as xp
else:
    import numpy as xp

def wrap(input_angle, dim=None):
    if isinstance(input_angle, xp.ndarray):
        if input_angle.size == 0:
            return input_angle
        else:
            angle = xp.array(input_angle)
    else:
        angle = input_angle
    
    if dim:
        angle[dim] -= 2*xp.pi * xp.floor((angle[dim] + xp.pi) / (2*xp.pi))
    else:
        angle -= 2*xp.pi * xp.floor((angle + xp.pi) / (2*xp.pi))
    return angle