from asyncio.windows_events import NULL
import csv
import string
import time
import random
import pandas as pd
from datetime import datetime, timedelta
import math

TEAM_ID = "1032" #FROM LAST YEAR
PACKET_TYPE = 67
PACKET_TYPE2 = 80
startTime = NULL

file = open('Flight_'+TEAM_ID+'.csv', 'w', newline='')

writer = csv.writer(file)

#TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE,
#HS_DEPLOYED, PC_DEPLOYED, MAST_RAISED, TEMPERATURE, VOLTAGE,
#GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS,
#TILT_X, TILT_Y, CMD_ECHO

writer.writerow(["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE", 
"HS_DEPLOYED", "PC_DEPLOYED", "MAST_RAISED", "TEMPERATURE", "VOLTAGE", 
"GPS_TIME", "GPS_ALTITUDE", "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_SATS",
"TILT_X", "TILT_Y", "CMD_ECHO", "T+ Time", "Acceleration"])

file.close()


i = 0
while i < 600:

    i+=1

    with open('Flight_'+TEAM_ID+'.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        rand = random.randint(0,100)
        rand2 = random.randint(0,100)
        rand3 = random.randint(0,100)
        rand4 = random.randint(0,100)
        rand5 = random.randint(0,100)
        rand6 = random.randint(0,100)
        rand7 = random.randint(0,100)
        rand8 = random.randint(0,100);
        if (i == 1):
            startTime = datetime.now()

        writer.writerow([TEAM_ID,datetime.now().strftime("%H:%M:%S"),i, 'F', 'LAUNCH_WAIT',
        rand7, 'N', 'N', 'N', rand5, rand, datetime.now().strftime("%H:%M:%S"), rand3, rand5,
        rand4, rand5, rand6, rand7, 'CXON' , str(math.floor((datetime.now()-startTime).total_seconds())), rand8])


    time.sleep(1)