#Filename: average_output.py
#Written by: Ryan Kinsey
#Description: The purpose of this program is to read table 'averagedata' from database 'master_test1.db' and output information into a csv file for evaluation

#Library Imports
import sqlite3		#This module provides an SQL interface
import csv		#This module implements classes to read/write to csv files

#Create a connection to the database
connection = sqlite3.connect('/home/sims/Database/master_test1.db')
cursor = connection.cursor()

#Notes
#1 minute = 120 datapoints

#List the database contents
cursor.execute("SELECT * FROM rawdata ORDER BY key DESC LIMIT 60")
recordset = cursor.fetchall()

#Declare CSV Writer, filename, and write permissions
#csvWriter = csv.writer(open("/home/sims/CSV/average_output_03302017.csv", "w"))

#Loop through the database and export the data row by row
for (key, timestamp, val0, val1, val2, val3) in recordset:
    print key,timestamp,val0,val1,val2,val3
#csvWriter.writerows(recordset)

#Commit the transaction and close the connection
connection.commit()
cursor.close()
connection.close()
