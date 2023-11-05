import csv
import numpy as np

import json

from pynput.mouse import Controller, Button
mouse = Controller()

from screeninfo import get_monitors
monitor = get_monitors()[0]
screen_size = (monitor.width, monitor.height)


def load_indexes_from_csv(file_path):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    
    header = data[0]
    indexes = list(map(list, zip(*[[int(value) for value in row] for row in data[1:]])))
    
    return {
        header[0]: indexes[0],
        header[1]: indexes[1],
        header[2]: indexes[2],
        header[3]: indexes[3]
    }

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

def read_from_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data

        
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
