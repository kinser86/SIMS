#Filename: config.py
#Written by: Ryan Kinsey
#Date: 03/29/2017
#Description: The purpose of this program help configure the sensors by turning on the desired sensor

#Library Imports
import serial	#Import the Serial Library
import time	#Import the Time Library

#Notes
#USB0 = sensor_right
#USB1 = sensor_front
#USB2 = sensor_back
#USB3 = sensor_left

#Declare Serial Port Parameters
port = serial.Serial("/dev/ttyUSB2", baudrate = 9600, timeout = None, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE)

#Loop to run continously
while True:
    list = []					#Array to hold data sample
    port.flushInput()
    for i in range(0,4):			#Loop 4 instances
        data_raw = port.read()			#Read the serial data
        #print('1: %s' % data_raw)
        data_string = str(data_raw)		#Convert the data into string
        data_hex = hex(ord(data_string))	#Convert the data into a hexadecimal
        data_int = int(data_hex, 0)		#Convert the data into an integer
        list.append(data_int)			#Append data to the array
    print(list)	#Print the array data
