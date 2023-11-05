import numpy as np
from utils import stream_helper

def calibrate(angle_list, target_angles=np.array([0,0,0])):
    # Calculate the offset between the target angles and the provided angles
    offset = target_angles - angle_list

    return offset

port = "/dev/cu.Remy"
stream = stream_helper(port)


