import numpy as np

def wrap(input_angle, dim=None):
    if isinstance(input_angle, np.ndarray):
        if input_angle.size == 0:
            return input_angle
        else:
            angle = np.array(input_angle)
    else:
        angle = input_angle
    
    if dim:
        angle[dim] -= 2*np.pi * np.floor((angle[dim] + np.pi) / (2*np.pi))
    else:
        angle -= 2*np.pi * np.floor((angle + np.pi) / (2*np.pi))
    return angle