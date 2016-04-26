
import csv
from datetime import datetime
import math
import pymysql
INPUT_FILENAME = "Nmea_Files/AttoPilot_Flight.txt"
OUTPUT_FILENAME = 'Csv_Files/'+INPUT_FILENAME[11:-4]+'.csv'
dbQuery='SELECT * FROM ex2.nmea;'

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')

cur=db.cursor()
cur.execute(dbQuery)
result=cur.fetchall()
c = csv.writer(open(OUTPUT_FILENAME, 'w'))
for row in result:
    c.writerow(row)
    