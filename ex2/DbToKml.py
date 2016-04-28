import sys
import pymysql
from _datetime import datetime

kml_start = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
<Document>
  <name>Track Log</name>
  <description>Route</description>
  <Style id="roadStyle">
    <LineStyle>
      <color>ff4444ff</color>
      <width>3</width>
    </LineStyle>
  </Style>
  <Placemark>
    <name>Route</name>
    <styleUrl>#roadStyle</styleUrl>
    <MultiGeometry>
      <LineString><coordinates>'''

kml_end = '''</coordinates></LineString>
    </MultiGeometry>
  </Placemark>
</Document>
</kml>'''

INPUT_FILENAME = "Nmea_Files/running.txt"
OUTPUT_FILENAME = 'Kml_Files/'+INPUT_FILENAME[11:-4]+'.kml'
try:
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')
    dbQuery='SELECT * FROM ex2.nmea;'
    cur=db.cursor()
    cur.execute(dbQuery)
    result=cur.fetchall()
except:
    print ("\tMySQL details error")
    sys.exit()
f= open(OUTPUT_FILENAME,'w')
f.write(kml_start)
for row in result:
    dat=row[0] 
    time=row[1]
    speed=row[2]
    lat=row[3]
    lon=row[4]
    f.write('%s,%s'%(lon,lat)+" ")
f.write(kml_end)    
f.close()


