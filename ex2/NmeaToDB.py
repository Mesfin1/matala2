 
import csv
import math
import pymysql
from datetime import datetime
INPUT_FILENAME = "Nmea_Files/AttoPilot_Flight.txt"
with open(INPUT_FILENAME, 'r') as input_file:
    reader = csv.reader(input_file)
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS nmea')
    #flag will tell us if the GPGGA is good if yes continue to the GPRMC
    flag = 0
    # Create table
   # c.execute('''create table ex2.db.ex
               #(date text,time text,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text)''')
    # create a csv reader object from the input file (nmea files are basically csv)
    
    c.execute('''create table nmea
             (date text,time text,speed float, latitude text, longitude text)''')
    # create a csv reader object from the input file (nmea files are basically csv)
   
    for row in reader:

            # skip all lines that do not start with $GPRMC
            if not (row[0].startswith('$GNRMC')) and not (row[0].startswith('$GPRMC')) :
                continue

            else:

                # for each row, fetch the values from the row's columns
                # columns that are not used contain technical GPS stuff that you are probably not interested in
                time = row[1]
               
                warning = row[2]
                latitude = row[3]
                lat_direction = row[4]
                longitude = row[5]
                lon_direction = row[6]
                speed = row[7]
                 
                
                date =  row[9]
                 
                tdate=datetime.strptime(date , '%d%m%y')
                tdate=tdate.strftime('%y-%m-%d')[:] 
                 
                
                
                tTime=datetime.strptime(time, '%H%M%S.%f')
                tTime=tTime.strftime('%H:%M:%S.%f')[:-7] 
                print("time "+tTime)
                
                # if the "warning" value is "V" (void), you may want to skip it since this is an indicator for an incomplete data row)
                if warning == 'V':
                    continue

                # merge the time and date columns into one Python datetime object (usually more convenient than having both separately)
                #date_and_time = datetime.strptime(date + ' ' + time, '%d%m%y %H%M%S.%f')

                # convert the Python datetime into your preferred string format, see http://www.tutorialspoint.com/python/time_strftime.htm for futher possibilities
                #date_and_time = date_and_time.strftime('%y-%m-%d %H:%M:%S.%f')[:-3] # [:-3] cuts off the last three characters (trailing zeros from the fractional seconds)

                # lat and lon values in the $GPRMC nmea sentences come in an rather uncommon format. for convenience, convert them into the commonly used decimal degree format which most applications can read.
                # the "high level" formula for conversion is: DDMM.MMMMM => DD + (YY.ZZZZ / 60), multiplicated with (-1) if direction is either South or West
                # the following reflects this formula in mathematical terms.
                # lat and lon have to be converted from string to float in order to do calculations with them.
                # you probably want the values rounded to 6 digits after the point for better readability.
                latitude = round(math.floor(float(latitude) / 100) + (float(latitude) % 100) / 60, 6)
                if lat_direction == 'S':
                    latitude = latitude * -1

                longitude = round(math.floor(float(longitude) / 100) + (float(longitude) % 100) / 60, 6)
                if lon_direction == 'W':
                    longitude = longitude * -1

                # speed is given in knots, you'll probably rather want it in km/h and rounded to full integer values.
                # speed has to be converted from string to float first in order to do calculations with it.
                # conversion to int is to get rid of the tailing ".0".
                speed = int(round(float(speed) * 1.852, 0))

                # write the calculated/formatted values of the row that we just read into the csv file
                c.execute("insert into nmea values (%s,%s,%s,%s,%s)",(date,time,speed, latitude, longitude))
                

        
       
    conn.commit()   
        
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
c.execute ("""select * from nmea""")

for row in c:
        print (row)

c.close()
 
conn.close()
 
 