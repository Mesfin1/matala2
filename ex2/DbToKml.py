
import sys
import pymysql
 

from _datetime import datetime
class K:
    kml_start = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
  <Document>
  <Placemark>
    <name>Route</name>
   <styleUrl>#roadStyle</styleUrl>
    <MultiGeometry>
    <LineString>
     <coordinates>\n'''
    
    kml_end = '''
     </coordinates>
     </LineString>
    </MultiGeometry>
  </Placemark>
  </Document>
</kml>'''
    
    
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')
    dbQuery='SELECT * FROM ex2.nmea;'
    cur=db.cursor()
    cur.execute(dbQuery)
    result=cur.fetchall()
    
    f= open('Kml_Files/r.kml','w')
    f.write(kml_start)
    for row in result:
        #maybe needed in the future
           #date=row[0] 
           #time=row[1]
           # speed=row[2] 
        lat=row[3]
        lon=row[4]
       
        f.write('\t%s,%s'%(lon,lat)+'\n')
    f.write(kml_end)
    f.close()

 




