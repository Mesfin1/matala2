
import csv
from datetime import datetime
import math
import pymysql
INPUT_FILENAME = "Nmea_Files/stockholm_walk.txt"
OUTPUT_FILENAME = 'Csv_Files/'+INPUT_FILENAME[11:-4]+'.csv'

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='da9352238g', db='ex2')
dbQuery='SELECT * FROM ex2.nmea;'

cur=db.cursor()
cur.execute(dbQuery)
result=cur.fetchall()
# create a csv writer object for the output file
c = csv.writer(open(OUTPUT_FILENAME, 'w'))
# write the header line to the csv file
c.writerow(['date','time', 'speed', 'lat', 'lon'])
for row in result:
    c.writerow(row)
    