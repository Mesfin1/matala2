
An extensible parser and encoder for NMEA-0183 sentences for use with python in eclipse (pydev)
If you are not familiar with NMEA-0183, look it up on Wikipedia 
https://en.wikipedia.org/wiki/NMEA_0183.

RMC - NMEA has its own version of essential gps pvt (position, velocity, time) data. It is called RMC, 
The Recommended Minimum, which will look similar to:
All NMEA messages start with the $ character, and each data field is separated by a comma.
for example:

$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A

Where:

     RMC          Recommended Minimum sentence C
     123519       UTC Time 12:35:19 
     A            Status A=active or V=Void.
     4807.038,N   Latitude 48 deg 07.038' N
     01131.000,E  Longitude 11 deg 31.000' E
     022.4        Speed over the ground in knots
     084.4        Track angle in degrees True
     230394       Date - 23rd of March 1994
     003.1,W      Magnetic Variation
     *6A          The checksum data, always begins with *
     
Features:

runs under eclipse (plugin pydev) and mysql workbench
parses individual NMEA-0183 sentences
has built-in support for several of the most common NMEA sentences
GPGGA,GPRMC,GNRMC

lets you add sentence parsers for those not built-in
takes geographic location input and encodes it into valid NMEA-0183 sentences

Primary Functions

with open(nmeaFile.txt, mode='r' or 'w' it depends what you want to do-> read,write)
open the nmea file and read the data from it by using this link
http://gis.stackexchange.com/questions/180523/nmea-to-csv-with-timestamp-using-gpsbabel

when we get all the data needed.
step to create the database:
we create schema (in our project its called ex2) in mysql that we want connect to.
every data that we get from nmea file we convert it to the same type for exsample date is DATE in mysql
and so on.
then we crate table in the same schema that we connected,every data is entity in the table 
after that just use the insert command
INSERT INTO table_name ( field1, field2,...fieldN ) VALUES ( value1, value2,...valueN )
to save to table use commit().

Source Code Content:

NmeaToDB.py parse the nmea data and insert to data base

DbToCsv.py  import the data from database to csv file that can be open in excel

DbToKml.py  import the data from database to kml file that can be seen in google earth
