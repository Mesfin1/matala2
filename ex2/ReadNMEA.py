 
def readNMEAFile(fileName):
    total_line =0
    total_gga=0
    xlist=[]
    for line in open(fileName,'r'):
        try:
            total_line+=1
            if('$GPGGA' not in line ):
                continue
            total_gga+=1
            arr=line.split(",")
            y=int(arr[2][:2])+float(arr[2][2:])/60.
            x=int(arr[4][:3])+float(arr[4][3:])/60.

            xlist.extend([x,y])
             
        except:
            print("Error")

    return xlist
def gga(da):
     ret = dict()
     if(da[0]=='$GPGGA' and len(da)==15):
         ret['utc_time']= da[1][0:2]+':'+da[1][2:4]+':'+da[1][4:]  
         ret['Latitude']=int(da[2][0:2])+(float(da[2][2:])/60)
         ret['Longitude']=da[2][0:2]+' '+da[2][2:]
         ret['ns']=da[3]
         ret['lon_deg']=int(da[4][0:3])+(float(da[4][3:])/60)
         ret['lon_dm']=da[4][0:3]+' '+da[4][3:]
         ret['ew']=da[5]
         ret['pfi']=da[6]
         ret['sat_used']=da[7]
         ret['hdop']=da[8]
         ret['msl_alt']=da[9]
         ret['alt_unit']=da[10]
         ret['geoid_sep']=da[11]
         ret['sep_unit']=da[12]
         ret['age_diff_cor']=da[13]
         ret['diff_ref_sta_id']=da[14][0:4]
         ret['csum']=da[14][4:]
     return ret;
 
fr=gga("C:/Users/Mesfin/Desktop/חשוב/שנה שנייה/מבנה תוכנה/nmea.txt")
print(fr)