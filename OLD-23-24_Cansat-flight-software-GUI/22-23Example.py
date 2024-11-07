from asyncio.windows_events import NULL
import PySimpleGUI as sg
import time
import os
import matplotlib.pyplot as plt 
from matplotlib.pyplot import figure 
from matplotlib import animation
import matplotlib as mpl
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
#from digi.xbee.devices import XBeeDevice
import csv
import serial

from pylab import *


brown = '#854803'
orange ='#f29411'

_VARS = {'window': False,
         'fig_agg0': False,
         'fig_agg1': False,
         'fig_agg2': False,
         'fig_agg3': False,
         'fig_agg4': False,
         'fig_agg5': False,
         'fig_agg6': False,
         'fig_agg7': False,

         'pltFig0': False,
         'pltFig1': False,
         'pltFig2': False,
         'pltFig3': False,
         'pltFig4': False,
         'pltFig5': False,
         'pltFig6': False,
         'pltFig7': False,

         'pltsubFig0': False,
         'pltsubFig1': False,
         'pltsubFig2': False,
         'pltsubFig3': False,
         'pltsubFig4': False,
         'pltsubFig5': False,           #Needed????
         'pltsubFig6': False,
         'pltsubFig7': False,

         'pltAxis0': False,
         'pltAxis1': False,
         'pltAxis2': False,
         'pltAxis3': False,
         'pltAxis4': False,
         'pltAxis5': False,
         'pltAxis6': False,
         'pltAxis7': False}

# Initialization of Variables

TEAM_ID = 1032
PT1 = 'U'
SS1 = 'U'
PC1 = 1
MODE = 'U'
HS_DEPLOY = 'U'
PC_DEPLOY = 'U'
MAST_RAISE = 'U'
CMD_ECHO = 'U'
GPS_SAT = 0
GPS_TIME = '00:00:00'
MISSION_TIME = '00:00:00'
internalpc = 0

simulationMode = True
simulationActivate = True



def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


directory = format(os.getcwd())

def clock():
    return (time.strftime("%H:%M:%S", time.gmtime()))

# First row of the GUI
top_banner = [[sg.Text('Team ID: '+str(TEAM_ID), font='Any 26', background_color='#1B2838', border_width=(5), size=(40), key = 'TEAM_ID'),
               sg.Text(MISSION_TIME, font='Any 22', background_color='#1B2838', border_width=(8), size=(10), key = 'missionTime'),
               sg.Button('Calibrate', font='Any 16'),
               sg.Button('Connect', font='Any 16'),
               sg.Button('Close', font='Any 16')]]

# Second row of the GUI 
second_row = [[sg.Text('PC DEPOY: '+ PC_DEPLOY, size=(14), font='Any 16', background_color='#1B2838', key = 'PC_DEPLOY'),
               sg.Text('Mode: '+ MODE, size=(13), font='Any 16', background_color='#1B2838', key = 'MODE'),
               sg.Text('GPS Time: ' + GPS_TIME, size=(18), font='Any 16', background_color='#1B2838', key='gpsTime'),
               sg.Text('Software State : '+SS1, size=(32), font='Any 16', background_color='#1B2838', key = 'STATE')]]

#Third row of the GUI 
third_row = [[sg.Text('Packet Count: '+str(PC1), size=(17), font='Any 16', background_color='#1B2838', key = 'PC1'),
               sg.Text('HS Deploy: '+HS_DEPLOY, size=(15), font='Any 16', background_color='#1B2838', key = 'HS_DEPLOY'),
               sg.Text('Mast Raised: '+MAST_RAISE, size=(15), font='Any 16', background_color='#1B2838', key = 'MAST_RAISED'),
               sg.Text('GPS Sat: ' +str(GPS_SAT), size=(13), font='Any 16', background_color='#1B2838', key = 'GPS_SAT'),
               sg.Text('CMD Echo: '+CMD_ECHO, size=(25), font='Any 16', background_color='#1B2838', key = 'CMD_ECHO')]]

#Fourth row of the GUI
fourth_row = [[sg.Canvas(key='figCanvas0'),
               sg.Canvas(key='figCanvas1'),
               sg.Canvas(key='figCanvas2'),
               sg.Canvas(key='figCanvas3'),]]

#Fifth row of the GUI
fifth_row = [[sg.Canvas(key='figCanvas5'),
              sg.Canvas(key='figCanvas6'),
              sg.Canvas(key='figCanvas7'),
              sg.Canvas(key='figCanvas4'),]]

#Sixth row of the GUI
sixth_row = [[sg.Text('CMD', size=(8), font = 'Any 26', background_color='#1B2838'),
              sg.Input(size=(30)),
              sg.Button('Send',size=(18), font='Any 16'),
              sg.Text(' '*100)]]

#Combines all the rows into one that will be displayed
layout = [[top_banner],
          [second_row],
          [third_row],
          [fourth_row],  #this is the graphs
          [fifth_row],   #this is also 5 graphs
          [sixth_row]]

_VARS['window'] = sg.Window('test window', layout, margins=(0,0), location=(0,0), finalize=True)

#TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE,
#HS_DEPLOYED, PC_DEPLOYED, MAST_RAISED, TEMPERATURE, VOLTAGE,
#GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS,
#TILT_X, TILT_Y, CMD_ECHO

#GPS TIME NEEDS TO BE PULLED FROM FILE. CURRENTLY IS NOT. 

def getPayloadData():

        global PC1
        global PT1
        global SS1
        global MODE
        global HS_DEPLOY
        global PC_DEPLOY
        global MAST_RAISE
        global CMD_ECHO
        global GPS_SAT 
        global GPS_TIME
        global MISSION_TIME
        global internalpc
        internalpc+=1


        if (internalpc > 8):
            data = pd.read_csv('Flight_1032.csv', header=None, names=["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE",
                "HS_DEPLOYED", "PC_DEPLOYED", "MAST_RAISED", "TEMPERATURE", "PRESSURE", "VOLTAGE",
                "GPS_TIME","GPS_LATITUDE", "GPS_LONGITUDE", 
                "GPS_ALTITUDE", "GPS_SATS","TILT_X", "TILT_Y", "CMD_ECHO"], skiprows=internalpc-8)
    
        else:
            data = pd.read_csv('Flight_1032.csv', header=None, names=["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE",
                "HS_DEPLOYED", "PC_DEPLOYED", "MAST_RAISED", "TEMPERATURE", "PRESSURE", "VOLTAGE",
                "GPS_TIME","GPS_LATITUDE", "GPS_LONGITUDE", 
                "GPS_ALTITUDE", "GPS_SATS","TILT_X", "TILT_Y", "CMD_ECHO"], skiprows=1)

        TEAM_ID = data['TEAM_ID'][len(data)-1]
        PC1 = data['PACKET_COUNT'][len(data)-1]
        SS1 = data['STATE'][len(data)-1]
        MODE = data['MODE'][len(data)-1]
        HS_DEPLOY = data['HS_DEPLOYED'][len(data)-1]
        PC_DEPLOY = data['PC_DEPLOYED'][len(data)-1]
        MAST_RAISE = data['MAST_RAISED'][len(data)-1]
        CMD_ECHO = data['CMD_ECHO'][len(data)-1]
        GPS_SAT = data['GPS_SATS'][len(data)-1]
        GPS_TIME = data['GPS_TIME'][len(data)-1]
        MISSION_TIME = data['MISSION_TIME'][len(data)-1]

        packetArray = data['PACKET_COUNT']
        altP = data['ALTITUDE']
        tempP = data['TEMPERATURE']
        voltP = data['VOLTAGE']
        gpsAlt = data['GPS_ALTITUDE']
        gpsLat = data['GPS_LATITUDE']
        gpsLong = data['GPS_LONGITUDE']
        tiltX = data['TILT_X']
        tiltY = data['TILT_Y']

        _VARS['window']['TEAM_ID'].update('Team ID: ' + str(TEAM_ID))
        _VARS['window']['PC1'].update('Packet Count : ' + str(PC1))
        _VARS['window']['STATE'].update('Software State : ' + str(SS1))

        _VARS['window']['MODE'].update('Mode : ' + str(MODE))
        _VARS['window']['HS_DEPLOY'].update('HS Deploy : ' + str(HS_DEPLOY))
        _VARS['window']['PC_DEPLOY'].update('PC Deploy : ' + str(PC_DEPLOY))
        _VARS['window']['MAST_RAISED'].update('Mast Raised : ' + str(MAST_RAISE))
        _VARS['window']['CMD_ECHO'].update('CMD Echo : ' + str(CMD_ECHO))
        _VARS['window']['GPS_SAT'].update('GPS Sat : ' + str(GPS_SAT))
        _VARS['window']['gpsTime'].update('GPS Time : ' + str(GPS_TIME))
        _VARS['window']['missionTime'].update(str(MISSION_TIME))


        return(packetArray, altP, tempP, voltP, gpsAlt, gpsLat, gpsLong, tiltX, tiltY)

def setyAxis():      #only done once in drawchart function to set axies
    _VARS['pltAxis0'].set_ylabel('Altitude')
    _VARS['pltAxis1'].set_ylabel('Temperature')
    _VARS['pltAxis2'].set_ylabel('Voltage')
    _VARS['pltAxis3'].set_ylabel('TiltX')
    _VARS['pltAxis4'].set_ylabel('TiltY')
    _VARS['pltAxis5'].set_ylabel('GPS Alt')
    _VARS['pltAxis6'].set_ylabel('GPS LAT')
    _VARS['pltAxis7'].set_ylabel('GPS LONG')
    #_VARS['pltAxis9'].set_ylabel('PE')
    
    _VARS['pltAxis0'].set_title('Altitude (m) vs Time(s)')
    _VARS['pltAxis1'].set_title('Temp (c) vs Time(s)')
    _VARS['pltAxis2'].set_title('Voltage volts) vs Time(s)')
    _VARS['pltAxis3'].set_title('TiltX (deg) vs Time(s)')
    _VARS['pltAxis4'].set_title('TiltY (deg) vs Time(s)')
    _VARS['pltAxis5'].set_title('GPS ALT (deg) vs Time(s)')
    _VARS['pltAxis6'].set_title('GPS LAT (deg) vs Time(s)')
    _VARS['pltAxis7'].set_title('GPS LONG (deg) vs Time(s)')
    #_VARS['pltAxis9'].set_title('Pointing Error (deg) vs Time (s)')

    _VARS['pltAxis0'].set_xlabel('Time')
    _VARS['pltAxis1'].set_xlabel('Time')
    _VARS['pltAxis2'].set_xlabel('Time')
    _VARS['pltAxis3'].set_xlabel('Time')
    _VARS['pltAxis4'].set_xlabel('Time')
    _VARS['pltAxis5'].set_xlabel('Time')
    _VARS['pltAxis6'].set_xlabel('Time')
    _VARS['pltAxis7'].set_xlabel('Time')
    #_VARS['pltAxis9'].set_xlabel('Time')

def drawChart(graph):  # graph is the graph number set as an integer  THIS CREATES THE GRAPHS AND DRAWS THEM BLANK
    _VARS['pltFig'+str(graph)] = plt.figure()
    _VARS['pltsubFig'+str(graph)] = plt.subplot()
    _VARS['pltAxis'+str(graph)] = plt.subplot()
    if (graph == 8):
        setyAxis()
    _VARS['pltAxis'+str(graph)].margins(0.05)  
    _VARS['pltFig'+str(graph)].set_size_inches(3.5,3.5)
    _VARS['fig_agg'+str(graph)] = draw_figure(
        _VARS['window']['figCanvas'+str(graph)].TKCanvas, _VARS['pltFig'+str(graph)])

i=0
while (i < 8):
    # Drawing 9 graphs
    drawChart(i)
    i+= 1


# Recreate Synthetic data, clear existing figre and redraw plot.

#create clock to keep track of frame in order to update graph??
#use panda to trigger new update in csv file and send to graph to update??
    

def updatePayloadChart():   #THIS TAKES ALL DATA AND GRAPHS IT

    # tPlusP, altP, tempP, voltP, gpsAlt, gpsLat, gpsLong, tiltX, tiltY

    payloadData = getPayloadData()

    packetArray = payloadData[0]
    payAlt = payloadData[1]
    payTemp = payloadData[2]
    payVolt = payloadData[3]
    gpsAlt = payloadData[4]
    gpsLat = payloadData[5]
    gpsLong = payloadData[6]
    tiltX = payloadData[7]
    tiltY = payloadData[8]

    _VARS['pltsubFig0'].cla()
    _VARS['pltsubFig1'].cla()
    _VARS['pltsubFig2'].cla()
    _VARS['pltsubFig3'].cla()
    _VARS['pltsubFig4'].cla()
    _VARS['pltsubFig5'].cla()
    _VARS['pltsubFig6'].cla()
    _VARS['pltsubFig7'].cla()
    #_VARS['pltsubFig9'].cla()

    _VARS['pltsubFig0'].plot(packetArray, payAlt, '-b')

    _VARS['pltsubFig1'].plot(packetArray, payTemp, '-b')

    _VARS['pltsubFig2'].plot(packetArray, payVolt, '-b')

    _VARS['pltsubFig3'].plot(packetArray, tiltX, '-k')

    _VARS['pltsubFig4'].plot(packetArray, tiltY, '-k')

    _VARS['pltsubFig5'].plot(packetArray, gpsAlt, '-b')

    _VARS['pltsubFig6'].plot(packetArray, gpsLat, '-r')

    _VARS['pltsubFig7'].plot(packetArray, gpsLong, '-r')

    setyAxis()

    _VARS['fig_agg0'].draw()
    _VARS['fig_agg1'].draw()
    _VARS['fig_agg2'].draw()
    _VARS['fig_agg3'].draw()
    _VARS['fig_agg4'].draw()
    _VARS['fig_agg5'].draw()
    _VARS['fig_agg6'].draw()
    _VARS['fig_agg7'].draw()
    #_VARS['fig_agg9'].draw()


# \\  -------- PYPLOT -------- //


_VARS['window'].maximize()


#updatePayloadChart()
i=0

fileLength = 0

#open up serial ports and such for Radio communication
ser = serial.Serial()
ser.baudrate = 19200
ser.port = 'COM4'
ser
ser.open()
print(ser)

file = open('Flight_'+str(TEAM_ID)+'.csv', 'w', newline='')

writer = csv.writer(file)

writer.writerow(["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE",
                "HS_DEPLOYED", "PC_DEPLOYED", "MAST_RAISED", "TEMPERATURE", "PRESSURE", "VOLTAGE",
                "GPS_TIME","GPS_LATITUDE", "GPS_LONGITUDE", 
                "GPS_ALTITUDE", "GPS_SATS","TILT_X", "TILT_Y", "CMD_ECHO"])

file.close()

currentTime = time.time()
simDataRead = False
currentIndex = 0
wait = False

while True:
    event, values = _VARS['window'].read(timeout=10)
    if event in (None, 'Close'):
        break
    with open('Flight_'+str(TEAM_ID)+'.csv', 'a', newline='') as file:
        writer = csv.writer(file)
            
        #continuously poll for data
        xbee_message = str("hh")
        if(ser.in_waiting >0):
            xbee_message = (ser.readline().decode('utf-8'))
        
            print(xbee_message)
            #write the row to the csv file
            xbee_message2=xbee_message.strip().split(',')
            writer.writerow(xbee_message2)

    if event in (None, 'Send'):
        #get the string from the input box
        print(values[0])
        currentTime = time.time()
        time.sleep(1)
        #send it through the radio
        ser.write(bytes(values[0],'utf-8'))
        if (values[0] == "CMD,1032,SIM,ENABLE"):
            simulationMode = True
        elif (values[0] == "CMD,1032,SIM,ACTIVATE"):
            simulationActivate = True
        elif (values[0] == "CMD,1032,SIM,DISABLE"):
            simulationMode = False
            simulationActivate = False
    
    if (simulationMode & simulationActivate):
        #read from the csv file line by line and send to payload at 1s
        if(wait == True):
            if (simDataRead == False):
                simData = (pd.read_csv('Sample_Flight.csv', header=0, names=["Pressure"])).to_numpy()
                #print (simData
                simDataRead = True
                currentTime = time.time()
            if (time.time() - currentTime > 3.00):
                newVal = str(simData[currentIndex])[1:]
                newVal = newVal[:-1]
                newstring = 'CMD,1032,SIM,' +newVal

                ser.write(bytes(newstring, 'utf-8'))
                print("CMD,1032,SIM,"+newVal) #just for testing purposes
                currentTime = time.time()
                currentIndex += 1
        else:
            wait = True
    


    #_VARS['window']['time'].update(clock())
    #_VARS['window']['gpsTime'].update('GPS Time: ' + clock())

     
    data = pd.read_csv('Flight_1032.csv', usecols = ["PACKET_COUNT"])       #checks to see if line has been added to canister csv file
    if (len(data) >  fileLength):
        fileLength = len(data)
        if(fileLength >5):
            updatePayloadChart()


_VARS['window'].close()

#https://github.com/PySimpleGUI/PySimpleGUI/tree/master/DemoPrograms

#Using pandas to only read a chunk of the data that we need::
#https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#iterating-through-files-chunk-by-chunk
