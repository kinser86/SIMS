#Filename: state_test.py
#Written by: Ryan Kinsey
#Date: 04/10/2017
#Description: The purpose of this program is to read database 'master.db' that is being populate by program 'read.py'.  
#             This program will take the average of the last 120 samples from each sensor then determine if the refrigeration
#             system  needs to be turned of or not.
#             1) If the average is below the threshold:
#                 a) status = 1
#                 b) refrigeration system will stay on
#                 c) program will output state data to 'averagedata' table in database 'master.db'
#                 d) program will loop every 60 seconds.
#             2) If the average is above the threshold:
#                 a) status = 0
#                 b) refrigeration system  will stop
#                 c) program will output state data to 'averagedata' table in database 'master.db'
#                 d) After 5 minutes, the program will loop again and determine the new status.

#Library Imports
import subprocess		#This module enables the spawn of new processes 
import time			#This module provides various time-related functions
import datetime			#This module supplies classes for manipulating dates and times in simple and complex ways
import RPi.GPIO as GPIO		#This module enables control to Raspberry Pi GPIO channels
import os			#This module provides a portable way of using operating system functionality
import sqlite3			#This module provides a SQL interface
import random			#This module implements pseudo-random numbers, used for prototyping
import logging                  #This module defines functions and classes which implement a flexible event logging system for applications and libraries
from collections import Counter	#This module adds sorting abilities

#Configure Logging
logging.basicConfig(filename = '/home/sims/Logs/04102017', level=logging.WARNING, format='%(asctime)s | %(levelname)s | %(message)s')
logging.warning('state_test.py program has started')

#GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)		#This is the first channel for the relay board
GPIO.setup(13,GPIO.OUT)		#This is the second channel for the relay board
GPIO.setup(31,GPIO.OUT)		#This LED color will be 'blue' and is used to signify function read_sate() is running
GPIO.setup(37,GPIO.OUT)		#This LED color will be 'white' and is used to signify function write_state() is running

#Program Constants
threshold = 20		#Initial refrigeration turn off threshold (Changes below depending on 'state' condition)

#Program Variables
state = 'None!'
return_array = 'None!'

#This function writes information to the 'averagedata' table in the database 'master.db'
def write_state(val0,val1,val2,val3,average,state):
    #Enable LED to signify the program is running
    GPIO.output(37,GPIO.HIGH)
    logging.debug('LED State: on')
    #Create a connection to the database
    logging.debug('Database Status:')
    logging.debug('....Connecting')
    connection = sqlite3.connect('/home/sims/Database/master_test1.db')
    logging.debug('....Connected')
    cursor = connection.cursor()
    #Add data to database
    logging.debug('....Writing')
    cursor.execute("INSERT INTO averagedata values(null, datetime('now','localtime'), (?), (?), (?), (?), (?), (?))",(val0,val1,val2,val3,average,state,))
    logging.debug('....Written')
    #Commit and close
    connection.commit()
    logging.debug('....Commited')
    cursor.close()
    connection.close()
    logging.debug('....Closed')

    #Disable LED to signify the program has completed
    GPIO.output(37,GPIO.LOW)
    logging.debug('LED State: off')

#This function reads the table 'rawdata' in database 'master.db', analyzes the information, and determines the system state. This function returns information.
def read_state():
    #Enable LED to signify the program is running
    GPIO.output(31,GPIO.HIGH)
    logging.debug('LED State: on')

    #Define arrays to be populated
    val0array = []	#Array can contain up to 120 elements
    val1array = []	#Array can contain up to 120 elements
    val2array = []	#Array can contain up to 120 elements
    val3array = []	#Array can contain up to 120 elements
    valall = []		#Array will contain 4 elements, each element the average of respectice valarray[n]
    logging.debug('Arrays Defined')
    logging.debug('Database Status:')
    logging.debug('....Connecting')
    #Create a connection to the database
    connection = sqlite3.connect('/home/sims/Database/master_test1.db')
    logging.debug('....Connected')
    #Collect the last 10 * entries from table 'rawdata' in database 'master.db'
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM rawdata ORDER BY key DESC LIMIT 10')
    logging.debug('....Collecting')
    valset = cursor.fetchall()
    logging.debug('....Collected')
    connection.commit()
    logging.debug('....Commited') 
    cursor.close()
    connection.close()
    logging.debug('....Closed')

    #Collect and arrange data for each sensor
    logging.debug('Data Status:')
    for (key, timestamp, val0, val1, val2, val3) in valset:
            val0array.append(val0)
            logging.debug('....val0 appended') 
            val1array.append(val1)
            logging.debug('....val1 appended')
            val2array.append(val2)
            logging.debug('....val2 appended')
            val3array.append(val3)
            logging.debug('....val3 appended')
    logging.debug('....Data appended')

    #Post process data
    #Determine the average for val0array with respect to the number of elements
    logging.debug('Processing: val0')
    val0_count = Counter(val0array)
    val0_out = val0_count.most_common(1)[0][0]
    logging.info('....val0: {}' .format(val0_out))
    valall.append(val0_out)
    logging.debug('....val0_out appended to valall')

    #Determine the average for val1array with respect to the number of elements
    logging.debug('Processing: val1')
    val1_count = Counter(val1array)
    val1_out = val1_count.most_common(1)[0][0]
    logging.debug('....val1: {}' .format(val1_out))
    valall.append(val1_out)
    logging.debug('....val1_out appended to valall')

    #Determine the average for val2array with respect to the number of elements
    logging.debug('Processing: val2')
    val2_count = Counter(val2array)
    val2_out = val2_count.most_common(1)[0][0]
    logging.debug('....val2t: {}' .format(val2_out))
    valall.append(val2_out)
    logging.debug('....val2_out appended to valall')

    #Determine the average for val3array with respect to the number of elements
    logging.debug('Processing: val3')
    val3_count = Counter(val3array)
    val3_out = val3_count.most_common(1)[0][0]
    logging.debug('....val3: {}' .format(val3_out))
    valall.append(val3_out)
    logging.debug('....val3_out appended to valall')

    #Determine the average for valall with respect to the number of elements
    logging.info('Processing: valall')
    valall_sum = sum(valall)
    logging.debug('....valall sum complete')
    valall_count = len(valall)
    logging.debug('....valall count complete')
    valall_average = valall_sum/valall_count
    logging.debug('....valall average complete')
    logging.info('....vallall average: {}' .format(valall_average))

    #Determine the state for the refrigeration system
    logging.debug('Processing: State')
    global state, threshold
    if (valall_average >= threshold):
        state = 1			#Keep the compressor on
        threshold = 20			#Make Ice Lower Bound
        logging.debug('....State = 1')
    else:
        state = 0			#Turn the compressor off
        threshold =  25			#Melt Ice Lower Bound(Previously 35)
        logging.debug('....State = 0')
    logging.debug('....complete')

    logging.debug('Compiling Status:')
    return_array = []
    logging.debug('....array defined')
    return_array.append(val0_out)
    logging.debug('....val0array_average appended')
    return_array.append(val1_out)
    logging.debug('....val1array_average appended')
    return_array.append(val2_out)
    logging.debug('....val2array_average appended')
    return_array.append(val3_out)
    logging.debug('....val3array_average appended')
    return_array.append(valall_average)
    logging.debug('....val0all_average appended')
    return_array.append(state)
    logging.debug('....state appended')

    return return_array 
 
    #Disable LED to signify the program has completed
    GPIO.output(31,GPIO.LOW)
    logging.debug('LED State: off')

#This function blinks an LED for visual reference
def idle_led(freq,t):
    for i in range (0,t):
        logging.info('....{}'.format(i))
        GPIO.output(31,GPIO.HIGH)
        time.sleep(0.50)
        GPIO.output(31,GPIO.LOW)
        time.sleep(0.50)

#Loop the program
#First let us determine the state of the machine
run = True
try:
    while (True):
        #First let us determine the state of the machine
        logging.debug('Reading...')
        state_array = read_state()

        #Average below threshold
        logging.info('System Status:')
        logging.debug('....calculating')
        if (state == 1):
            logging.info('....State = 1')
            #Keep relays closed
            logging.info('Relay State:')
            GPIO.output(11,GPIO.LOW)
            GPIO.output(13,GPIO.LOW)
            logging.info('....CLOSED')
            #Run program which writes the system state to 'averagedata' table
            logging.debug('....writing to database')
            write_state(state_array[0], state_array[1], state_array[2], state_array[3], state_array[4], state_array[5])
            logging.debug('....writing completed')
            logging.info('Sleep for 60 seconds')
            idle_led(2,60)
        else:
            logging.info('....State = 0')
            #Keep relays open
            logging.info('Relay State:')
            GPIO.output(11,GPIO.HIGH)
            GPIO.output(13,GPIO.HIGH)
            logging.info('....OPEN')
            #Run program which writes the system state to 'averagedata' table
            logging.debug('....writing to database')
            write_state(state_array[0], state_array[1], state_array[2], state_array[3], state_array[4], state_array[5])
            logging.debug('....writing completed')
            logging.info('Sleep for 300 seconds')
            GPIO.output(37,GPIO.LOW)
            idle_led(2,300)

except KeyboardInterrupt:
    logging.debug('Done')
    logging.warning('state_test.py program interrupted')
except:
    logging.warning('state_test.py program crash!')
    os.system('sudo reboot -f')
finally:
    GPIO.cleanup()
