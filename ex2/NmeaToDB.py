 
import csv,sys,os.path
import math
import pymysql

#the nmea file that we will get the data from 

INPUT_FILENAME = 'Nmea_Files/house.txt'

with open(INPUT_FILENAME,'r') as input_file:
    reader = csv.reader(input_file) 
    try:
        #connection to mysql server
        DBconn = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mes307Fin', db='ex2')
        c = DBconn.cursor()
        
        #delete the table if its exists 
        c.execute('DROP TABLE IF EXISTS nmea')
    
        #create the table 
        c.execute('''create table nmea
                 (Date DATE,Time TIME,Speed float , Latitude text,North_South text, Longitude text,East_West text)''')
        print("Done create nmea table")
    except :
        print ("\tMySQL details error")
        sys.exit()
    
    
    else:
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
                
                    #find date in format yyyy-mm-dd 
                    yyyy=date[4:]
                    mm=date[2:4]
                    dd=date[0:2]
                    tdate='%s-%s-%s' % (yyyy, mm, dd)
                 
                    #find latitude degree and latitude minute
                    latDegrees=latitude[0:2]
                    latMinute=latitude[2:]
                    
                    #find latitude degree and latitude minute
                    lonDegrees=longitude[0:3]
                    lonMinute=longitude[3:]
               
                    #find time in format hh:mm:ss
                    hours = time[0:2]
                    minutes = time[2:4]
                    seconds = time[4:6]
              
                    tTime='%s:%s:%s' % (hours, minutes, seconds)
                    
                    # if the "warning" value is "V" (void), you may want to skip it since this is an indicator for an incomplete data row)
                    if warning == 'V':
                        continue
    
                    # lat and lon have to be converted from string to float in order to do calculations with them.
                    # you probably want the values rounded to 6 digits after the point for better readability.
                    latitude=round(float(latDegrees)+float(latMinute)/60,6)
                     
                    if lat_direction == 'S':
                        latitude = latitude * -1
    
                    longitude=round(float(lonDegrees)+float(lonMinute)/60,6)
                  
                    if lon_direction == 'W':
                        longitude = longitude * -1
    
                    # speed is given in knots, you'll probably rather want it in km/h and rounded to full integer values.
                    # speed has to be converted from string to float first in order to do calculations with it.
                    # conversion to int is to get rid of the tailing ".0".
                   
                    if speed[0:] == '':
                        speed=0
                    else:
                        speed = int(float(speed) * 1.852)
            
                    # write the calculated/formatted values of the row that we just read into the csv file
                    try:
                        c.execute("insert into nmea values (%s,%s,%s,%s,%s,%s,%s)",(tdate,tTime,speed, latitude,lat_direction, longitude,lon_direction))
                      
                    except :
                        print ("insert into nmea table error")
                        sys.exit()
        
        #save the changes to database
        try:
            DBconn.commit()
            print("Save/Insert Success!")
        except :
          print ("Save To MySQL error")
          sys.exit()
        DBconn.close()  
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

input_file.close()


  
 
 