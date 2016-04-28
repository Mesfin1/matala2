
import csv
from datetime import datetime
import math
import pymysql
<<<<<<< HEAD
INPUT_FILENAME = "Nmea_Files/f.txt"
OUTPUT_FILENAME = 'Csv_Files/f.csv'
=======
INPUT_FILENAME = "Nmea_Files/stockholm_walk.txt"
OUTPUT_FILENAME = 'Csv_Files/'+INPUT_FILENAME[11:-4]+'.csv'
>>>>>>> refs/remotes/origin/master

<<<<<<< HEAD
 
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')
=======
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='sql pass', db='ex2')
dbQuery='SELECT * FROM ex2.nmea;'
>>>>>>> refs/remotes/origin/master

dbQuery='SELECT * FROM ex2.nmea;'
cur=db.cursor()
cur.execute(dbQuery)
result=cur.fetchall()
<<<<<<< HEAD

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
     
=======
# create a csv writer object for the output file
c = csv.writer(open(OUTPUT_FILENAME, 'w'))
# write the header line to the csv file
c.writerow(['date','time', 'speed', 'lat', 'lon'])
for row in result:
    c.writerow(row)
    
>>>>>>> refs/remotes/origin/master
