
import csv
from datetime import datetime
import math
import pymysql
INPUT_FILENAME = "Nmea_Files/f.txt"
OUTPUT_FILENAME = 'Csv_Files/f.csv'

 
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')

dbQuery='SELECT * FROM ex2.nmea;'
cur=db.cursor()
cur.execute(dbQuery)
result=cur.fetchall()

# create a csv writer object for the output file and write the header
try:
    c = csv.writer(open(OUTPUT_FILENAME, 'w'))
    c.writerow(['  date','  time', '  speed', '  latitude', '  longitude'])
    for row in result:
        c.writerow(row)
except IOError:
    print ("Could not open file! Please close Excel!")

cur.close()
db.close()
     