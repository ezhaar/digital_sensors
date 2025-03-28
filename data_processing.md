# GNSS

## IOT EDGE format

### Header
```csv
id,gga utc timestamp,latitude,latitude hemisphere,longitude,longitude hemisphere,quality,satellites in use,horizontal dilution of precision,orthometric height,orthometric height unit,geoid separation,geoid separation unit,differential gps age,station and checksum,id,heading in degrees,true north and checksum,id,zda utc timestamp,day,month,year,hour offset from gmt,minute offset from gmt and checksum
```
### Data
```csv
$GPGGA,000000.00,3842.1157054,S,14627.9002501,E,1,43,0.4,9.2670,M,-3.9017,M,,*6E,$GPHDT,277.718,T*39,$GPZDA,000000.00,19,03,2025,,*68
$GPGGA,080306.00,3842.1160043,S,14627.9002727,E,1,47,0.4,11.0887,M,-3.9017,M,,*5E,$GPHDT,277.546,T*30,$GPZDA,080307.00,22,03,2025,,*6C
```

## Jesper's Script
### Header
None

### Data
```csv
20250314T130001_012 $GPZDA,130001.00,14,03,2025,,*66
20250314T130001_145 $GPGGA,130001.00,3842.1160316,S,14627.9002051,E,1,47,0.4,9.0270,M,-3.9017,M,,*6E
```


gga_DataTimeStamp_UTC,GGA_Lat,GGA_Dir_of_Lat,GGA_Long,GGA_Dir_of_Long,GGA_QualityIndicator,GGA_No_of_SV,GGA_HDOP,GGA_OrthometricHeight,GGA_unit_of_measure,GGA_Geoid_Seperation,GGA_Geoid_Seperation_meters,GGA_Age_of_DGPS,GGA_Ref_Station,id,heading in degrees,true north and checksum,id,zda utc timestamp,day,month,year,hour offset from gmt,minute offset from gmt and checksum
