
import sys
import fileinput
from sys import stdout
from collections.__main__ import Point

template_before = '''<?xml version="1.0" encoding="UTF-8"?>
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
    <MultiGeometry>\n'''

template_after = '''    </MultiGeometry>
  </Placemark>
</Document>
</kml>\n'''

def findCoordinates(v):
    t = v.split('.')
    var=int(t[0][:-2]) + (int(t[0][-2:]) + int(t[1]) / (10.0 ** len(t[1]))) / 60
 
    return var

def conToKml(input):
    result = []
    for s in input:
        t = s.split(',')
        if ((t[0] != '$GPGGA')and(t[0] != '$GNGGA')) or (t[2] == '') or (t[4] == '') or (t[9] == ''):
            continue
        result.append('%.7f,%.7f,%s' % (findCoordinates(t[4]), findCoordinates(t[2]), t[9]))
        print(result)
    return result

def write_output(points):
    
    file = 'Kml_Files/AttoPilot' + '.kml'
    FILE = open(file, 'w')
    FILE.write(template_before)
    FILE.write('      <LineString><coordinates>%s</coordinates> </LineString>\n' % ' '.join(points))
    FILE.write(template_after)
  
def main():
    argv= 'Nmea_Files/AttoPilot Flight  2008-12-02.txt' 
    write_output(conToKml(fileinput.input(argv)))

if __name__ == "__main__":
    main()
    
    
    