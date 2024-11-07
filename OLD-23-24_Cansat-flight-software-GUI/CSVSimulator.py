import csv
import pandas as pd
from datetime import datetime
import random
import numpy as np
import time
import os

now = datetime.now()

df = pd.DataFrame(np.empty((0, 21)))

df.columns = ["TEAM_ID","MISSION_TIME","PACKET_COUNT","MODE","STATE","ALTITUDE","AIR_SPEED","HS_DEPLOYED","PC_DEPLOYED","TEMPERATURE",
              "PRESSURE","VOLTAGE","GPS_TIME","GPS_ALTITUDE","GPS_LATITUDE","GPS_LONGITUDE","GPS_SATS","TILT_X","TILT_Y",
              "ROT_Z","CMD_ECHO"]

df.loc[0] = [2031, str(datetime.now())[11:][:-7],1,"S","LAUNCH_WAIT",random.randint(1,100),
                                       random.randint(1,101),"N","N",random.randint(1,100),random.randint(1,100),random.randint(1,100),
                                       str(datetime.now())[11:][:-7],random.randint(1,100),random.randint(1,100),random.randint(1,100),random.randint(1,101),
                                       random.randint(1,100),random.randint(1,100),random.randint(1,100),"CXON"]

packet_count = 2

while(packet_count <= 1000):
    start = time.perf_counter()
    df.loc[len(df.index)] = [2031, str(datetime.now())[11:][:-7],packet_count,"S","LAUNCH_WAIT",random.randint(1,100),
                                       random.randint(1,100),"N","N",random.randint(1,100),random.randint(1,100),random.randint(1,100),
                                       str(datetime.now())[11:][:-7],random.randint(1,100),random.randint(1,100),random.randint(1,100),random.randint(1,101),
                                       random.randint(1,100),random.randint(1,100),random.randint(1,100),"CXON"]
    # print(df)
    packet_count+=1
    time.sleep(1.0)

    df.to_csv("SimCSV.csv")
    end = time.perf_counter()
    duration = round(end - start, 5)
    print(f'Time to push data: {duration} seconds')

os.remove("SimCSV.csv")