import pandas as pd
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import time
import csv
import serial



class Cansat:
    def __init(self, csv_file_path):
        self.packet = {
            'TEAM_ID': 2031, 
            'MISSION_TIME': '00:00:00', # UTC time in hh:mm:ss
            'PACKET_COUNT': 0, # The total count of transmitted packets since turned on reset to zero by command when the CanSat is installed in the rocket on the launch pad at the beginning of the mission and maintained through processor reset.
            'MODE': 'S', # 'F' for flight mode and 'S' for simulation mode.
            'STATE': 'U', # The operation state of the software. (LAUNCH_WAIT, ASCENT, ROCKET_SEPERATION, DESCENT, HS_RELEASE, LANDED, etc).
            'ALTITUDE': 0, # In units of meters and must be relative to ground level at the launch site. 
            'AIR_SPEED': 0, # In meters/second measured with the pitot tube during both ascent and descent.
            'TEMPERATURE' : 0,
            'PRESSURE' : 0,
            'VOLTAGE': 0, # Voltage of the Cansat power bus 
            'GYRO_R' : 0, # 'P' indicates the heat shield is deployed, 'N' otherwise.
            'GYRO_P' : 0, # 'C' indicates he parachute is deployed (at 100m), 'N' otherwise. 
            'GYRO_Y' : 0, 
            'ACCEL_R' : 0,
            'ACCEL_P' : 0,
            'ACCEL_Y' : 0,
            'MAG_R' : 0,
            'MAG_P' : 0,
            'MAG_Y' : 0,
            'Auto_Gyro_Rotation_Rate' : 0,
            'GPS_TIME': '00:00:00', # In UTC. Time from the GPS reciever. 
            'GPS_ALTITUDE': 0, # In meters. The altitude from the GPS reciever above mean sea level.
            'GPS_LATITUDE': 0, # In degrees North. The latitude from the GPS reciever.
            'GPS_LONGITUDE': 0, # In degrees West. The longitude from the GPS reciever.
            'GPS_SATS': 0, # In int. Number of GPS satellites being tracked by the GPS reciever. 
            'CMD_ECHO': "CXON" # Text of the last command recieved and processed by the CanSat.
        }

        self.csv_file_path = csv_file_path