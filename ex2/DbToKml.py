import sys
import pymysql
from _datetime import datetime

kml_start='''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
 <Document>
  <Style id="linestyleExample">
    <LineStyle>
      <color name="orangered">#FF4500</color>
      <width>5</width>
      <gx:labelVisibility>2</gx:labelVisibility>
    </LineStyle>
  </Style>
  <Placemark>
    <LineString>
     <altitudeMode>absolute</altitudeMode>
      <coordinates>\n'''

kml_end=''' </coordinates>
    </LineString>
  </Placemark>
 </Document>
</kml>
'''

INPUT_FILENAME = "Nmea_Files/Ariel2.txt"
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
    lat=row[3]
    lon=row[5]
    f.write('%s,%s\n'%(lon,lat)+" ")
    
f.write(kml_end)    
f.close()


