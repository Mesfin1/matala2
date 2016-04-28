 
from collections import Counter
from datetime import datetime
import csv
import os
import random
import subprocess
import sys

version = "0.2"
path = "c:\\tools\\"

# color legend
c_brownish  = "ff0055ff"
c_darkblue  = "ffff0000"
c_green     = "ff00ff00" 
c_lightblue = "ffffaa55"
c_mustard   = "ff00aaaa"
c_pink      = "fff8a5f8"
c_red       = "ff0000ff"
c_violet    = "ffaa00ff"
c_white     = "ffffffff"
c_yellow    = "ff00ffff"

colors = [c_red, c_yellow, c_violet, c_green, c_pink, c_brownish, c_white, c_darkblue, c_mustard, c_lightblue]

def welcome():
    os.system('cls')
    try:
        subprocess.check_output(path + 'exiftool.exe')
    except:
        print "\n\n ERROR: missing executable exiftool.exe\n\n\n"
        sys.exit()
    if len(sys.argv) == 1:
        print "\n\n geotag2kml v%s\n\n" % version
        print " How to use: ==> " + os.path.basename(sys.argv[0]) + " AbsolutePathToFolder"
        print "\n (no double quotes required)\n (the same path will be used to write the Google Earth KML file)\n\n"
        sys.exit()
    elif len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]) == True:
            os.chdir(sys.argv[1])
        else:
            print "\n ERROR: the path %s doesn't exist" % sys.argv[1]
            sys.exit()
 
welcome() 

start_time = datetime.now()

if os.path.exists('exif.csv'):
    os.remove('exif.csv')
elif os.path.exists('temp_exif.csv'):
    os.remove('temp_exif.csv')

#run exiftool tool recursively seeking for specific extensions and skipping files without the fields gpslongitude and datetimeoriginal
#csv output tab delimited

# http://www.sno.phy.queensu.ca/~phil/exiftool/exiftool_pod.html
# -ext EXT    (-extension)         Process files with specified extension
# -if EXPR                         Conditionally process files
# defined                          if condition is True
# ref tags:
#          exif:gpslongitude
#          exif:DateTimeOriginal
# -r                               Recursive search
# -gpslongitude# -gpslatitude#    Print coordinates in Decimal Degrees - without # output is Degrees Minutes Seconds
# (http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/GPS.html)
# chosen fields in the csv output:
# -datetimeoriginal -filename -directory -gpslongitude# -gpslatitude# -gpsaltitude -make -model
# -T          (-table)             Output in tabular format

os.system(path + 'exiftool.exe * -ext jpg -ext jpeg -ext tif -ext tiff -if "defined $exif:gpslongitude" -if "defined $exif:DateTimeOriginal" -r -datetimeoriginal -filename -directory -gpslongitude# -gpslatitude# -gpsaltitude -make -model -T >> temp_exif.csv')

#sort csv by DateTimeOriginal
with open('temp_exif.csv', 'r') as r:
    with open('exif.csv', 'w') as w:
        w.write("datetimeoriginal\tfilename\tdirectory\tgpslongitude\tgpslatitude\tgpsaltitude\tmake\tmodel\n")
        for line in sorted(r):
            w.write(line)

r.close()
os.remove('temp_exif.csv')
w.close()

with open('exif.csv', 'r') as r:
    numlines=len(r.readlines())-1

r.close()

#find unique dates. This information will be used to name folders        
reader = csv.DictReader(open("exif.csv"), delimiter='\t')

uniq_dates  = []
uniq_models = []

for line in reader:
    a = line["datetimeoriginal"]
    a = a[:10] # YYYY:MM:DD
    uniq_dates.append(a,)
    b = line["make"] + " " + line["model"]
    uniq_models.append(b)
    
uniq_dates          = sorted(set(uniq_dates))
uniq_models_counter = Counter(uniq_models) #number of pics by device model
uniq_models         = sorted(set(uniq_models))


# kml_start contains the first block of data of the KML file

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
    <MultiGeometry>\n'''

# Create KML file

if os.path.exists('GoogleEarth.kml'):
    os.remove('GoogleEarth.kml')
    w = open('GoogleEarth.kml','w')
    w.write(kml_start)
else:
    w = open('GoogleEarth.kml','w')
    w.write(kml_start)

# COLUMN LAYOUT REMINDER
# column[0] = DateTimeOriginal
# column[1] = Filename
# column[2] = Directory
# column[3] = GPSLongitude
# column[4] = GPSLatitude
# column[5] = GPSAltitude
# column[6] = Make
# column[7] = Model
# 
# GPSAltitudeRef
# 0 = Above Sea Level
# 1 = Below Sea Level
# http://www.sno.phy.queensu.ca/~phil/exiftool/faq.html


# write placemarks

def sea_level(refvalue):
    if refvalue.find('Above') != -1:
        return(refvalue[:refvalue.find('Above')-1] + " A")
    else:
        return(refvalue[:refvalue.find('Below')-1] + " B")

counter_wp_date = 0
for date in uniq_dates:
    w.write("<Folder>\n")
    w.write("\t<name>%s</name>\n" % date)
    counter_wp_date    += 1   #counter_wp_date increases every time date in uniq_dates changes
    counter_1stwp_date  = 0
    w.write("\t<open>%d</open>\n" % counter_wp_date)
    for line in open("exif.csv"):
        column = line.split("\t")
        if date in line:
            counter_1stwp_date += 1
            w.write("        <Placemark>\n")
            w.write("\t\t\t<name>%s *** %s %s *** (%s) *** %s</name>\n" % (column[0], column[6], column[7].rstrip('\n'), sea_level(column[5]),column[1]))
            w.write("\t\t\t<description>\n\t\t\t<![CDATA[<table><tr><td>\n")
            w.write("\t\t\t<img src='%s/%s' width='384' height='288'>\n\t\t\t</td></tr></table>]]>\n\t\t\t</description>\n" % (column[2].lower(),column[1].lower()))
            if counter_1stwp_date == 1:    # value 1 means that it's the first waypoint of a new path (shown with the icon of a man)
                w.write("\t\t\t<styleUrl>#msn_man</styleUrl>\n\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (column[3],column[4]))
            else:
                w.write("\t\t\t<styleUrl>#msn_pink-blank</styleUrl>\n\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (column[3],column[4]))
            if counter_wp_date <=10:
                color=colors[counter_wp_date-1]
            else:
                color=random.choice(colors)
            w.write("\n        </Placemark>\n")
    w.write('''        <Placemark>
            <name>Path %s on-off</name>
            <description>Path %s</description>
            <Style>
             <LineStyle>
               <color>%s</color>
               <width>4.0</width>
             </LineStyle>
            </Style>
            <MultiGeometry> 
              <LineString>
              <tessellate>%d</tessellate>
                <coordinates>''' % (date,date,color,counter_wp_date))  #choose a random color for each path line
    for line in open("exif.csv"):
        column = line.split("\t")
        if date in line:
            w.write(str(column[3]) + "," + str(column[4]).rstrip('\n') + ",0\t")
    w.write('''
               </coordinates>
              </LineString>
            </MultiGeometry> 
        </Placemark>''')
    w.write("\n</Folder>\n")

#kml_end = KML file footer
kml_end = "</Document>\n</kml>"
w.write(kml_end)
w.close()

#print successful message

if len(uniq_models)==1:
    print "\n\n Geotagged photos (%d in total) were taken with:\n" % numlines
else:
    print "\n\n Geotagged photos (%d in total) were taken with %d different devices:\n" % (numlines, len(uniq_models))
for makemodel, freq in uniq_models_counter.most_common():
    print " -  %s (%d)" % (makemodel,freq)

print "\n\n Google Earth KML file was successfully created!!\n"

end_time = datetime.now()
print "\n\nScript started : " + str(start_time)
print "Script finished: " + str(end_time)
print('Duration       : {}'.format(end_time - start_time))