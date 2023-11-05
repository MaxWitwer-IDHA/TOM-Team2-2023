# from utils import pull_data
# from pynput.mouse import Controller
# mouse = Controller()


# while True:
#     data = pull_data()
#     parsed_data = [float(val) for val in data.split(",")]
#     print(parsed_data)

# import numpy as np
# from utils import stream_helper, calibrate, move_mouse



# port = "/dev/cu.Remy"
# stream = stream_helper(port)

# offset = calibrate(stream)
# print(offset)

# while True:
#     bluetooth_dump = stream.pull_data()
#     button_state = bluetooth_dump[-1]
#     coordinates = np.array(bluetooth_dump[0:3])
#     angle_radians = np.deg2rad(coordinates)
#     renormalized = np.arcsin(np.sin(angle_radians))

#     move_mouse(renormalized[0] - offset[0], renormalized[2] - offset[2])




from pynput.mouse import Controller, Button
from mouse_utils import stream_helper, calibrate, move_mouse

port = "/dev/cu.Remy"
stream = stream_helper(port)
mouse = Controller()

hold_counter = 0
move_check = 0
threshold = 35  # Set your desired threshold here (number of time steps)
distance_threshold = 1  # Set your desired distance threshold here

previous_position = mouse.position  # Store the initial mouse position

print("connected")

while True:
    bluetooth_dump = stream.pull_data()
    button_state = bluetooth_dump[-1]

    if button_state == 1:  # Assuming 1 represents a button press
        mouse.press(Button.left)  # Press the left mouse button
        if move_check != 1:
            hold_counter += 1
    else:
        mouse.release(Button.left)  # Release the left mouse button
        if hold_counter >= threshold:
            mouse.click(Button.right, 1)  # Simulate a right mouse click
        hold_counter = 0  # Reset the counter
        move_check = 0

    # Check for mouse movement
    current_position = mouse.position
    if abs(current_position[0] - previous_position[0]) > distance_threshold or \
       abs(current_position[1] - previous_position[1]) > distance_threshold:
        move_check = 1  # Reset the counter if movement exceeds threshold

    previous_position = current_position





    # coordinates = np.array(bluetooth_dump[0:3])
    # angle_radians = np.deg2rad(coordinates)
    # renormalized = np.arcsin(np.sin(angle_radians))
    
