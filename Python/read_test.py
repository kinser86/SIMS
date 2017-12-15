#Filename: read_test.py
#Written by: Ryan Kinsey
#Date: 04/09/2017
#Description: The purpose of this program is the read sensor inputs and then write them to the database 'master.db'.

#Library imports
import subprocess		#This module enables the spawn of new processes
import time			#This module provides various time-related functions
import datetime			#This module supplies classes for manipulating dates and times in simple and complex ways
import RPi.GPIO as GPIO		#This module enables control to Raspberry Pi GPIO channels
import os			#This module provides a portable way of using operating system functionality
import sqlite3			#This module provides a SQL interface
import random			#This module implements pseudo-random numbers. Used only for prototyping
import logging			#This module defines functions and classes which implement a flexible event logging system for applications and libraries
import serial			#This module enables access to the serial port

#Configure Logging
logging.basicConfig(filename = '/home/sims/Logs/04102017.txt', level=logging.WARNING, format='%(asctime)s | %(levelname)s | %(message)s')
logging.warning('read_test.py program has started')

#GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.OUT)		#LED color 'green' to signify the program is running
GPIO.setup(38,GPIO.OUT)		#LED color 'yellow' to signify program is writing to the database

#Write to sqlite3 database
def log_state(val0,val1,val2,val3):
    #Enable LED to signify the program is running
    GPIO.output(38,GPIO.HIGH)
    logging.debug('Database Status:')
    logging.debug('....Connecting to master(rawdata)')
    #Create a connection to the database
    connection = sqlite3.connect('/home/sims/Database/master_test1.db')
    logging.debug('....Connected to master(rawdata)')
    cursor = connection.cursor()
    #Add data to database
    logging.debug('....Writing to master(rawdata)')
    cursor.execute("INSERT INTO rawdata values(null, datetime('now','localtime'), (?), (?), (?), (?))",(val0,val1,val2,val3,))
    logging.debug('....Written to master(rawdata)')
    #Commit and close
    connection.commit()
    logging.debug('....Commited to master(rawdata)')
    cursor.close()
    connection.close()
    logging.debug('....Closed connection with master(rawdata)')
    
    #Disable LED to signify the program has completed
    GPIO.output(38,GPIO.LOW)

#Read port0
def port0_read():
    global list
    GPIO.output(36,GPIO.HIGH)	#Turn on the LED to signify the program is running
    port_data = []
    logging.debug('Initializing Collection: port0')
    logging.debug('port0: connecting to /dev/ttyUSB0')
    port = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = None, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE)
    logging.debug('port0: connected')
    logging.debug('port0: collecting')
    i = 1
    while (i == 1):
        port.flushInput()
        port.flushOutput()
        for j in range(0,4):                    #Loop 4 instances
            data_raw = port.read()              #Read the serial data
            data_string = str(data_raw)         #Convert the data into string
            data_hex = hex(ord(data_string))    #Convert the data into a hexadecimal
            data_int = int(data_hex, 0)         #Convert the data into an integer
            port_data.append(data_int)          #Append data to the array
        logging.debug('port0: verifying data')
        if (port_data[0] != 255):
            port_data = []
            logging.debug('port0: bad data, recollecting')
            i = 1
            time.sleep(0.100)
        else:
            logging.debug('{}' .format(port_data))
            logging.debug('port0: good data, continue')
            i = 0
    list.append(port_data[1])
    port.close()
    logging.debug('port0: connection closed')
    GPIO.output(36,GPIO.LOW)
    time.sleep(1.000)

#Read port1
def port1_read():
    GPIO.output(36,GPIO.HIGH)	#Turn on the LED to signify the program is running
    port_data = []
    logging.debug('Initializing Collection: port1')
    logging.debug('port1: connecting to /dev/ttyUSB1')
    port = serial.Serial("/dev/ttyUSB1", baudrate = 9600, timeout = None, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE)
    logging.debug('port1: connected')
    logging.debug('port1: collecting')
    i = 1
    while (i == 1):
        port.flushInput()
        port.flushOutput()
        for j in range(0,4):                    #Loop 4 instances
            data_raw = port.read()              #Read the serial data
            data_string = str(data_raw)         #Convert the data into string
            data_hex = hex(ord(data_string))    #Convert the data into a hexadecimal
            data_int = int(data_hex, 0)         #Convert the data into an integer
            port_data.append(data_int)          #Append data to the array
        logging.debug('port1: verifying data')
        if (port_data[0] != 255):
            port_data = []
            logging.debug('port1: bad data, recollecting')
            i = 1
            time.sleep(0.100)
        else:
            logging.debug('{}' .format(port_data))
            logging.debug('port1: good data, continue')
            i = 0
    list.append(port_data[1])
    port.close()
    logging.debug('port1: connection closed')
    GPIO.output(36,GPIO.LOW)
    time.sleep(1.000)

#Read port2
def port2_read():
    GPIO.output(36,GPIO.HIGH)	#Turn on the LED to signify the program is running
    port_data = []
    logging.debug('Initializing Collection: port2')
    logging.debug('port2: connecting to /dev/ttyUSB2')
    port = serial.Serial("/dev/ttyUSB2", baudrate = 9600, timeout = None, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE)
    logging.debug('port2: connected')
    logging.debug('port2: collecting')
    i = 1
    while (i == 1):
        port.flushInput()
        port.flushOutput()
        for j in range(0,4):                    #Loop 4 instances
            data_raw = port.read()              #Read the serial data
            data_string = str(data_raw)         #Convert the data into string
            data_hex = hex(ord(data_string))    #Convert the data into a hexadecimal
            data_int = int(data_hex, 0)         #Convert the data into an integer
            port_data.append(data_int)          #Append data to the array
        logging.debug('port2: verifying data')
        if (port_data[0] != 255):
            port_data = []
            logging.debug('port2: bad data, recollecting')
            i = 1
            time.sleep(0.100)
        else:
            logging.debug('{}' .format(port_data))
            logging.debug('port2: good data, continue')
            i = 0
    list.append(port_data[1])
    port.close()
    logging.debug('port2: connection closed')
    GPIO.output(36,GPIO.LOW)
    time.sleep(1.000)
    
#Read port3
def port3_read():
    GPIO.output(36,GPIO.HIGH)	#Turn on the LED to signify the program is running
    port_data = []
    logging.debug('Initializing Collection: port3')
    logging.debug('port3: connecting to /dev/ttyUSB3')
    port = serial.Serial("/dev/ttyUSB3", baudrate = 9600, timeout = None, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE)
    logging.debug('port3: connected')
    logging.debug('port3: collecting')
    i = 1
    while (i == 1):
        port.flushInput()
        port.flushOutput()
        for j in range(0,4):                    #Loop 4 instances
            data_raw = port.read()             #Read the serial data
            data_string = str(data_raw)         #Convert the data into string
            data_hex = hex(ord(data_string))    #Convert the data into a hexadecimal
            data_int = int(data_hex, 0)         #Convert the data into an integer
            port_data.append(data_int)         #Append data to the array
        logging.debug('port3: verifying data')
        if (port_data[0] != 255):
            port_data = []
            logging.debug('port3: bad data, recollecting')
            i = 1
            time.sleep(0.100)
        else:
            logging.debug('{}' .format(port_data))
            logging.debug('port3: good data, continue')
            i = 0
    list.append(port_data[1])
    port.close()
    logging.debug('port3: connection closed')
    GPIO.output(36,GPIO.LOW)
    time.sleep(1.000)

#Loop
run = True
try:
    while (True):
        list = []		#Create blank array for data to append to
        port0_read()		#Read port0
        port1_read()		#Read port1
        port2_read()		#Read port2
        port3_read()		#Read port3
        
        #Write the data to the database
        log_state(list[0],list[1],list[2],list[3])	#Write the information to the database for sensor
        logging.info('Output: {}, {}, {}, {}' .format(list[0],list[1],list[2],list[3]))
        #print list

except KeyboardInterrupt:
    print "Done"
    logging.warning('read_test.py program interrupted')
except:
    logging.warning('read_test.py program crash!')
    os.system('sudo reboot -f')
finally:
    GPIO.cleanup()
