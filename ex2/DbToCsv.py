import csv
import sys
import math
import pymysql

INPUT_FILENAME = "Nmea_Files/running.txt"
OUTPUT_FILENAME = 'Csv_Files/'+INPUT_FILENAME[11:-4]+'.csv'
global  result
global  cur
try:
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')
    dbQuery='SELECT * FROM ex2.nmea;'
    cur=db.cursor()
    cur.execute(dbQuery)
    result=cur.fetchall()
  
except :
    print ("\tMySQL details error")
    sys.exit()
try:
    c = csv.writer(open(OUTPUT_FILENAME, 'w'))
    c.writerow(['  date','  time', '  speed', '  latitude', '  longitude'])
    for row in result:
        c.writerow(row)
    cur.close()
    db.close()
except IOError:
    print ("Could not open file! Please close Excel!")

     