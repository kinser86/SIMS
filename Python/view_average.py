#Filename: average_output.py
#Written by: Ryan Kinsey
#Description: The purpose of this program is to read table 'averagedata' from database 'master_test1.db' and output information into a csv file for evaluation

#Library Imports
import sqlite3		#This module provides an SQL interface
import csv		#This module implements classes to read/write to csv files
import time

#Create a connection to the database
connection = sqlite3.connect('/home/sims/Database/master_test1.db')
cursor = connection.cursor()

#Notes
#1 hour = 60 datapoints

#List the database contents
cursor.execute("SELECT * FROM averagedata ORDER BY key DESC LIMIT 30")
recordset = cursor.fetchall()

#Declare CSV Writer, filename, and write permissions
#csvWriter = csv.writer(open("/home/sims/CSV/average_output_03302017.csv", "w"))

#while True:
    #Loop through the database and export the data row by row
for (key, timestamp, val0, val1, val2, val3, average, state) in recordset:
    print key,timestamp,val0,val1,val2,val3,average,state
    #csvWriter.writerows(recordset)
print('Done')
    #time.sleep(60)

#Commit the transaction and close the connection
connection.commit()
cursor.close()
connection.close()
