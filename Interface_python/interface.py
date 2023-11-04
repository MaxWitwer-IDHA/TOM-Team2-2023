# from utils import pull_data
# from pynput.mouse import Controller
# mouse = Controller()


# while True:
#     data = pull_data()
#     parsed_data = [float(val) for val in data.split(",")]
#     print(parsed_data)

import serial

# Replace the port with your device's port
port = "/dev/cu.HC-06"
baud_rate =  38400

# Define the serial port
ser = serial.Serial(port, baud_rate)

try:
    while True:
        # # Read data from the user to send to the device
        # data_to_send = input("Enter data to send (or 'exit' to quit): ")

        # # Exit the loop if the user enters 'exit'
        # if data_to_send == 'exit':
        #     break

        # # Send the data to the device
        # ser.write(data_to_send.encode())

        # Read and print the echo back from the device
        echo = ser.readline().decode()
        print(f"Device echo: {echo}", end='')

except KeyboardInterrupt:
    pass

# Close the serial port when done
ser.close()
