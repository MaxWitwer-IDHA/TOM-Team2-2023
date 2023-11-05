
import serial
import numpy as np

from pynput.mouse import Controller
mouse = Controller()

class stream_helper():
    def __init__(self, port, baud=115200):
        self.ser = serial.Serial(port, baud) 


    def pull_data(self):  
        try:
            data = self.ser.readline().decode().strip().split(",")
            collector = [float(val) for val in data]
            return collector

        except KeyboardInterrupt:
            data = None
            self.ser.close()
            print("Serial connection closed.")
            return data

        except:
            return None

def calibrate(stream):
    collector = []
    for i in range(150):
        # Pull data from the stream and convert to radians
        coordinates = np.array(stream.pull_data()[0:3])
        angle_radians = np.deg2rad(coordinates)

        # Apply renormalization
        renormalized = np.arcsin(np.sin(angle_radians))
        collector.append(renormalized)

    # Calculate average angles along each axis
    avg_angles = np.mean(np.array(collector), axis=0)

    return avg_angles

def move_mouse(angle_x, angle_y, speed_base=15, speed_linear=15, threshold=0.1):
    dist_center = np.sqrt(angle_y**2 + angle_x**2)

    if dist_center > threshold:
        speed_multiply = (speed_base**(dist_center-threshold))*speed_linear
        
        adjust_x = angle_x*speed_multiply
        adjust_y = angle_y*speed_multiply

        current_x, current_y = mouse.position
        new_x = np.clip(current_x - adjust_x, 0, screen_size[0])
        new_y = np.clip(current_y - adjust_y, 0, screen_size[1])

        mouse.position = (new_x, new_y)