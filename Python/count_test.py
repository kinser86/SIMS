#Filename: count_test.py
#Written by: Ryan Kinsey
#Date: 04/10/2017
#Description: The purpose of this program is to collect data from the database
#             then arrange based on the frequency of the number

#Library Imports
import sqlite3
from collections import Counter

#Declare Variables
val0array = []		#Array can contain up to 120 elements
val1array = []		#Array can contain up to 120 elements
val2array = []		#Array can contain up to 120 elements
val3array = []		#Array can contain up to 120 elements

#Program Constants
filter_low = 20		#Lower boundry in filtering the data read
filter_high = 110	#Upper boundry in filtering the data read

#Create a connection to the database
connection = sqlite3.connect('/home/sims/Database/master_test1.db')
cursor = connection.cursor()

#List the database contents
cursor.execute("SELECT * FROM rawdata ORDER BY key DESC LIMIT 200")
valset = cursor.fetchall()

for (key, timestamp, val0, val1, val2, val3) in valset:
    val0array.append(val0)
    val1array.append(val1)
    val2array.append(val2)
    val3array.append(val3)				

data0 = Counter(val0array)
data_out0 = data0.most_common(3)

data1 = Counter(val1array)
data_out1 = data1.most_common(3)

data2 = Counter(val2array)
data_out2 = data2.most_common(3)

data3 = Counter(val3array)
data_out3 = data3.most_common(3)

print data_out0
print data_out1
print data_out2
print data_out3

#Commit the transaction and close the connection
connection.commit()
cursor.close()
connection.close()
