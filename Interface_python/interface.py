
import serial
import time

port = '/dev/cu.usbserial-B000DUMD'

# Define the serial port and baud rate (make sure it matches your Arduino)
ser = serial.Serial(port, 115200)  # Change 'COM3' to the appropriate serial port


def pull_data():  
    try:
        data = ser.readline().decode().strip()
    except KeyboardInterrupt:
        data = None
        ser.close()
        print("Serial connection closed.")

    return data

