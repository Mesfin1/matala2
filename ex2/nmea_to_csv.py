
import csv
from datetime import datetime
import math
import pymysql
INPUT_FILENAME = "Nmea_Files/WorktoHome.txt"
OUTPUT_FILENAME = 'Csv_Files/'+INPUT_FILENAME[11:-4]+'.csv'
dbQuery='SELECT * FROM ex2.nmea;'

<<<<<<< HEAD
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')
=======
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='sql password', db='ex2')
>>>>>>> branch 'master' of https://github.com/Mesfin1/matala2.git

cur=db.cursor()
cur.execute(dbQuery)
result=cur.fetchall()
# create a csv writer object for the output file
c = csv.writer(open(OUTPUT_FILENAME, 'w'))
# write the header line to the csv file
c.writerow(['date','time', 'lat', 'lon', 'speed'])
for row in result:
    c.writerow(row)
    