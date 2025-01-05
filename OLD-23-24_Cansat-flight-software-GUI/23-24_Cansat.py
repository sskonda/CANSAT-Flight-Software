# 23-24 CanSat Source Code
# Team Lead: Steele Elliott

# Members: 
# Danush Singla
# Sarah Tran 
# Matthew Lee 
# Alex Segelnick
# Dylan Manauasa
# Sanat Konda

import pandas as pd
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import csv
import serial

# Define a consistent color scheme and fonts
# Updated color constants
PRIMARY_COLOR = '#09103d'  # Dark background color for the GUI
TEXT_COLOR = 'white'  # Text color for GUI elements on the primary background
GRAPH_BACKGROUND_COLOR = 'white'  # White background color for graphs
GRAPH_TEXT_COLOR = 'white'  # Text color for graph labels, titles, and axes

# Font definitions
FONT_TITLE = ('Helvetica', 17)
FONT_MAIN = ('Helvetica', 14)
FONT_BUTTON = ('Helvetica', 12)

sg.theme_background_color(PRIMARY_COLOR)

class CanSat:
    def __init__(self, csv_file_path):
        self.data = {
            'TEAM_ID': 2031, 
            'MISSION_TIME': '00:00:00', # UTC time in hh:mm:ss
            'PACKET_COUNT': 0, # The total count of transmitted packets since turned on reset to zero by command when the CanSat is installed in the rocket on the launch pad at the beginning of the mission and maintained through processor reset.
            'MODE': 'S', # 'F' for flight mode and 'S' for simulation mode.
            'STATE': 'U', # The operation state of the software. (LAUNCH_WAIT, ASCENT, ROCKET_SEPERATION, DESCENT, HS_RELEASE, LANDED, etc).
            'ALTITUDE': 0, # In units of meters and must be relative to ground level at the launch site. 
            'AIR_SPEED': 0, # In meters/second measured with the pitot tube during both ascent and descent.
            'HS_DEPLOYED': 'N', # 'P' indicates the heat shield is deployed, 'N' otherwise.
            'PC_DEPLOYED': 'N', # 'C' indicates he parachute is deployed (at 100m), 'N' otherwise. 
            'TEMPERATURE': 0, # In degrees Celsius
            'PRESSURE': 0, # In kPa. Air pressure of the censor used. 
            'VOLTAGE': 0, # Voltage of the Cansat power bus 
            'GPS_TIME': '00:00:00', # In UTC. Time from the GPS reciever. 
            'GPS_ALTITUDE': 0, # In meters. The altitude from the GPS reciever above mean sea level.
            'GPS_LATITUDE': 0, # In degrees North. The latitude from the GPS reciever.
            'GPS_LONGITUDE': 0, # In degrees West. The longitude from the GPS reciever.
            'GPS_SATS': 0, # In int. Number of GPS satellites being tracked by the GPS reciever. 
            'TILT_X': 0, # In angle degrees of the CanSat on the x-axis.
            'TILT_Y': 0, # In angle degrees of the CanSat on the y-axis.
            'ROT_Z': 0, # In degrees/second. The rotation rate of the CanSat.
            'CMD_ECHO': "CXON" # Text of the last command recieved and processed by the CanSat.
        }
        self.csv_file_path = csv_file_path

        # Initialized so that the program don't crash
        self.df = '0'

        # Checks to see if the csv exists before trying to start updating variables.
        try:
             f = open(self.csv_file_path)
             self.df = pd.read_csv(self.csv_file_path) # Checks to see if the csv file exists.
        except OSError:
            print("Could not open/read file:", self.csv_file_path) 

        self.graph_canvases = {}
        self.layout = self.create_gui_layout()
        self.window = sg.Window('CanSat Dashboard', self.layout, background_color=PRIMARY_COLOR, finalize=True)
        self.window.Maximize()
        self.window.TKroot.resizable(True, True)
        self.window.move(0, 0)

        # self.internalpc is what row the computer is on. This is used to make sure that the row being read actually exists in CSV file
        if(len(self.df) < 1):
            self.internalpc = 1
        else:
            self.internalpc = len(self.df)

        self.simulation_mode = False  # Simulation mode flag
            
        # Initializes graphs
        fig_size = (self.window.size[0]/350, self.window.size[1]/250) # Change the numerator in order to change the size of the graphs. 
        self.graphs = {
            'altitude': plt.subplots(figsize=(fig_size)),
            'air_speed': plt.subplots(figsize=(fig_size)),
            'temperature': plt.subplots(figsize=(fig_size)),
            'pressure': plt.subplots(figsize=(fig_size)),
            'voltage': plt.subplots(figsize=(fig_size)),
            'gps_altitude': plt.subplots(figsize=(fig_size)),
            'gps_latitude': plt.subplots(figsize=(fig_size)),
            'gps_longitude': plt.subplots(figsize=(fig_size)),
            'tilt_x': plt.subplots(figsize=(fig_size)),
            'tilt_y': plt.subplots(figsize=(fig_size)),
            'rot_z': plt.subplots(figsize=(fig_size))
        }
        for key, (fig, ax) in self.graphs.items():
            ax.set_facecolor(GRAPH_BACKGROUND_COLOR)
            ax.tick_params(colors=GRAPH_TEXT_COLOR)
            ax.xaxis.label.set_color(GRAPH_TEXT_COLOR)
            ax.yaxis.label.set_color(GRAPH_TEXT_COLOR)
            ax.title.set_color(GRAPH_TEXT_COLOR)
            fig.patch.set_facecolor(PRIMARY_COLOR)
            fig.subplots_adjust(left=0.15, bottom=0.25, right=0.85, top=0.90)

            # Create canvas as before
            canvas = FigureCanvasTkAgg(fig, master=self.window[f'graph_canvas_{key}'].TKCanvas)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill='both', expand=True)
            self.graph_canvases[key] = (canvas, canvas_widget)
    
    def create_top_banner(self):
        # NOTE: Things like <PRESSURE> will not have values manually inputted, it would be automatically read from the CSV.
        dropdown_options = ["CMD,2031,CX,ON", "CMD,2031,CX,OFF", "CMD,2031,SIM,ENABLE", "CMD,2031,SIM,ACTIVATE", "CM,2031,SIM,DISABLE", "CMD,2031,ST,<UTC_TIME>", "CMD,2031,SIM,<PRESSURE>", "CMD,2031,CAL", "CMD,2031,BCN,ON", "CMD,2031,BCN,OFF"]
        return [
            sg.Text('Team ID: ' + str(self.data['TEAM_ID']), font=FONT_TITLE, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(15, 1), justification='left', key='TEAM_ID', pad=(0, 0)),
            sg.Text(self.data['MISSION_TIME'], font=FONT_TITLE, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='MISSION_TIME', pad=(0, 0)),
            sg.Button('Simulation Mode', font=FONT_BUTTON, key='Sim_Mode', image_filename="button_simulate_edited.png", border_width=0, button_color=PRIMARY_COLOR, pad=(5, 0)),
            sg.Button(font=FONT_BUTTON, button_color=PRIMARY_COLOR, border_width=0, image_filename="close_button_edited.png", pad=(5, 0), expand_x=True, expand_y = False),
            sg.Text("Eggsplorer rocks!!!!", text_color=PRIMARY_COLOR, background_color=PRIMARY_COLOR), # Just extra text to make CMD section right justified 
            sg.Text('Input', font=(FONT_MAIN, 20), background_color=PRIMARY_COLOR, size=(5, 1), text_color=TEXT_COLOR, justification='right', pad=(0,0)),
            sg.DD(dropdown_options, font=(FONT_MAIN, 20), size=(26, 15), pad=(0,0)),
            sg.Button('Send', font=FONT_BUTTON, size=(5, 1), pad=(0,0))
        ]
    
    def create_second_row(self):
        return [
            sg.Text('PC DEPLOY: ' + self.data['PC_DEPLOYED'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='PC_DEPLOYED', pad=(0, 0)),
            sg.Text('Mode: ' + self.data['MODE'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='MODE', pad=(0, 0)),
            sg.Text('GPS Time: ' + self.data['GPS_TIME'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(25, 1), justification='left', key='GPS_TIME', pad=(0, 0)),
            sg.Text('Software State: ' + self.data['STATE'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='STATE', pad=(0, 0))
        ]

    def create_third_row(self):
        return [
            sg.Text('Packet Count: ' + str(self.data['PACKET_COUNT']), font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='PC1', pad=(0, 0)),
            sg.Text('HS Deploy: ' + self.data['HS_DEPLOYED'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='HS_DEPLOYED', pad=(0,0)),
            sg.Text('GPS Sat: ' + str(self.data['GPS_SATS']), font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(25, 1), justification='left', key='GPS_SATS', pad=(0,0)),
            sg.Text('CMD Echo: ' + self.data['CMD_ECHO'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='CMD_ECHO', pad=(0,0))
        ]

    def create_fourth_row(self):
        graph_size = (300, 300)  # Adjust size as needed
        return [
            sg.Canvas(key='graph_canvas_altitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_air_speed', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_temperature', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_pressure', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0))
        ]

    def create_fifth_row(self):
        graph_size = (250, 250)  # Adjust size as needed
        return[
            sg.Canvas(key='graph_canvas_voltage', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_gps_altitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_gps_latitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_gps_longitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0))
        ]

    def create_sixth_row(self):
        graph_size = (250, 250)  # Adjust size as needed
        return[
            sg.Text("Eggsplorer rocks!!! Go Gators!!!", text_color=PRIMARY_COLOR, background_color=PRIMARY_COLOR), # Just extra text to make this row of graphs centered.
            sg.Canvas(key='graph_canvas_tilt_x', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_tilt_y', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_rot_z', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0))
        ]

    def create_gui_layout(self):
        layout = [
            [sg.Column([self.create_top_banner()], pad=(4,4), element_justification='center')],
            [sg.Column([self.create_second_row()], pad=(4,4), element_justification='center')],
            [sg.Column([self.create_third_row()], pad=(4,4), element_justification='center')],
            [sg.Column([self.create_fourth_row()], pad=(4,4), element_justification='center', expand_x=True, expand_y=True)],
            [sg.Column([self.create_fifth_row()], pad=(4,4), element_justification='center', expand_x=True, expand_y=True)],
            [sg.Column([self.create_sixth_row()], pad=(4,4), element_justification='center', expand_x=True, expand_y=True)],
        ]
        return layout   
    
    # Reads the latest row of the csv
    def read_latest_csv_data(self, data_one_col):
        if self.simulation_mode:
            pass
    
        # Checks to see if there are more than 7 rows into the CSV yet. 
        if (len(data_one_col) > 7):
            # > than 7 rows in the CSV so only the last 7 rows are read
            last_rows = pd.read_csv(self.csv_file_path, header=None, names=["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE",
                "AIR_SPEED", "HS_DEPLOYED", "PC_DEPLOYED", "TEMPERATURE", "PRESSURE", "VOLTAGE",
                "GPS_TIME","GPS_LATITUDE", "GPS_LONGITUDE", 
                "GPS_ALTITUDE", "GPS_SATS","TILT_X", "TILT_Y", "ROT_Z", "CMD_ECHO"], skiprows=len(data_one_col)-7)
        else:
            # <= 7 rows in the CSV, just skips the header row. 
            last_rows = pd.read_csv(self.csv_file_path, header=None, names=["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE",
                "AIR_SPEED", "HS_DEPLOYED", "PC_DEPLOYED", "TEMPERATURE", "PRESSURE", "VOLTAGE",
                "GPS_TIME","GPS_LATITUDE", "GPS_LONGITUDE", 
                "GPS_ALTITUDE", "GPS_SATS","TILT_X", "TILT_Y", "ROT_Z", "CMD_ECHO"], skiprows=1)

        graph_data = {
            'time': last_rows['MISSION_TIME'].tolist(),
            'packet_count': last_rows['PACKET_COUNT'].tolist(),
            'mode': last_rows['MODE'].tolist(),
            'state': last_rows['STATE'].tolist(),
            'altitude': last_rows['ALTITUDE'].tolist(),
            'air_speed': last_rows['AIR_SPEED'].tolist(),       # does not exist in Flight_1032.csv hence the error
            'hs_deployed': last_rows['HS_DEPLOYED'].tolist(),
            'pc_deployed': last_rows["PC_DEPLOYED"].tolist(),
            'temperature': last_rows['TEMPERATURE'].tolist(),
            'pressure': last_rows['PRESSURE'].tolist(),
            'voltage': last_rows['VOLTAGE'].tolist(),
            'gps_time': last_rows['GPS_TIME'].tolist(),
            'gps_altitude': last_rows['GPS_ALTITUDE'].tolist(),
            'gps_latitude': last_rows['GPS_LATITUDE'].tolist(),
            'gps_longitude': last_rows['GPS_LONGITUDE'].tolist(),
            'gps_sat': last_rows["GPS_SATS"].tolist(),
            'tilt_x': last_rows['TILT_X'].tolist(),
            'tilt_y': last_rows['TILT_Y'].tolist(),
            'rot_z': last_rows['ROT_Z'].tolist(),
            'cmd_echo': last_rows['CMD_ECHO'].tolist()
            # Add any additional fields you need
        }
        return graph_data
    
    # Updates all the graphs on the GUI
    def update_graphs(self, new_data):
        self.data["MISSION_TIME"] = str(new_data["time"][-1])
        self.data["PACKET_COUNT"] = str(new_data["packet_count"][-1])
        self.data["MODE"] = str(new_data['mode'][-1])
        self.data["STATE"] = str(new_data["state"][-1])
        self.data["HS_DEPLOYED"] = str(new_data["hs_deployed"][-1])
        self.data["PC_DEPLOYED"] = str(new_data["pc_deployed"][-1])
        self.data["GPS_TIME"] = str(new_data["gps_time"][-1])
        self.data["GPS_SATS"] = str(new_data["gps_sat"][-1])
        self.data["CMD_ECHO"] = str(new_data['cmd_echo'][-1])

        for key, (fig, ax) in self.graphs.items():
            ax.clear()
            if key in new_data and 'time' in new_data and len(new_data[key]) == len(new_data['time']):
                formatted_key = key.replace('_', ' ').upper()  # Format the key by replacing underscores with spaces and capitalizing each word.

                ax.plot(new_data['time'], new_data[key], color='black')
                ax.set_title(f'{formatted_key} VS TIME', color=GRAPH_TEXT_COLOR, fontweight='bold')

                ax.set_xlabel('TIME (s)', color=GRAPH_TEXT_COLOR)

                if formatted_key == "ALTITUDE":
                    formatted_key += " (m)"
                elif formatted_key == "TEMPERATURE":
                    formatted_key += " (c)"
                elif formatted_key == "VOLTAGE":
                    formatted_key += " (volts)"
                elif formatted_key == "AIR SPEED":
                    formatted_key += " (m/s)"
                elif formatted_key == "PRESSURE":
                    formatted_key += " (Pa)"
                else:
                    formatted_key += " (deg)"
                ax.set_ylabel(formatted_key, color=GRAPH_TEXT_COLOR)  # Use formatted key here
                
                # Set the title with bold font
                
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
            self.graph_canvases[key][0].draw()

        # Displays all the new graphs
        for key, (fig, ax) in self.graphs.items():
            canvas, canvas_widget = self.graph_canvases[key]
            canvas.draw()
    
    # Updates any text-based data at the top of the GUI
    def update_header_elements(self):
        self.window['TEAM_ID'].update('Team ID: ' + str(self.data['TEAM_ID']))
        self.window['MISSION_TIME'].update('Mission Time: ' + self.data['MISSION_TIME'])
        self.window['PC1'].update('Packet Count: ' + str(self.data['PACKET_COUNT']))
        self.window['MODE'].update('Mode: ' + self.data['MODE'])
        self.window['STATE'].update('Software State: ' + self.data['STATE'])
        self.window['PC_DEPLOYED'].update('PC Deploy: ' + self.data['PC_DEPLOYED'])
        self.window['HS_DEPLOYED'].update('HS Deploy: ' + self.data['HS_DEPLOYED'])
        self.window['GPS_SATS'].update('GPS Sat: ' + str(self.data['GPS_SATS']))
        self.window['GPS_TIME'].update('GPS Time: ' + self.data['GPS_TIME'])
        self.window['CMD_ECHO'].update('CMD Echo: ' + self.data['CMD_ECHO'])


    def run_gui(self):
        # create the serial port for radio communication
        ser = serial.Serial()
        ser.baudrate = 19200
        ser.port = 'COM5'
        ser
        ser.open()
        # print(ser)

        # create the initial csv file and write the header
        file = open(self.csv_file_path, 'w', newline='')
        writer = csv.writer(file)

        writer.writerow(["TEAM_ID","MISSION_TIME","PACKET_COUNT","MODE","STATE","ALTITUDE","AIR_SPEED","HS_DEPLOYED","PC_DEPLOYED","TEMPERATURE",
                "PRESSURE","VOLTAGE","GPS_TIME","GPS_ALTITUDE","GPS_LATITUDE","GPS_LONGITUDE","GPS_SATS","TILT_X","TILT_Y",
                "ROT_Z","CMD_ECHO"])
        
        file.close()


        while True:

            # check for new incomming message from radio
            with open(self.csv_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                    
                #continuously poll for data
                xbee_message = str("hh")
                if(ser.in_waiting >0):
                    try:
                        xbee_message = (ser.readline().decode('utf-8'))
                
                        print(xbee_message)
                        #write the row to the csv file
                        xbee_message2=xbee_message.strip().split(',')
                        writer.writerow(xbee_message2)
                    except:
                        print("Error reading in packet.")


            start_time = time.perf_counter()
            event, values = self.window.read(timeout=50) # Change int to adjust timing reading in the file.

            read_time = time.perf_counter()
            duration = round(read_time-start_time, 5)

            if event == sg.WIN_CLOSED or event == '':
                break

            if event == 'Sim_Mode': # Change this to Sim_Mode to get this branch to work
                self.simulation_mode = not self.simulation_mode
                print(f"Simulation Mode {'Enabled' if self.simulation_mode else 'Disabled'}")

            if event == "Send":
                print("Send Button Pressed")
                print(values[0])
                time.sleep(1)
                #send it through the radio
                ser.write(bytes(values[0],'utf-8'))

            # Read and graphs with new data                
            try:
                data_one_col = pd.read_csv(self.csv_file_path, usecols=["PACKET_COUNT"]) # Checks to see if the csv file can be read.
            except:
                print("CAN'T READ") # If it can't be read, skips everything below this line.
                continue

            # Correct way to read in data, change filename for simluation mode
            if (len(data_one_col) > self.internalpc):
                self.internalpc = len(data_one_col)
                
                # Reads the latest row of data
                new_data = self.read_latest_csv_data(data_one_col) # Function defintion at Line 198
                new_data_time = time.perf_counter()
                duration = round(new_data_time-start_time, 5)

                # Update header elements
                self.update_graphs(new_data) # Function definition at Line 172
                update_graphs_time = time.perf_counter()
                duration = round(update_graphs_time-new_data_time, 5)

                # Update header elements
                self.update_header_elements() # Function defintion at Line 237
                end_time = time.perf_counter()
                duration = round(end_time-start_time, 5)
            
        self.window.close()

def main():
    # Use SimCSV.csv if you are able to run the python skit alongside the VSCode
    # Else use Sample_Flight.csv
    csv_file_path = "Flight_2031.csv" # Have it depend on the mode. I think we might have to create a csv file here too?
    cansat = CanSat(csv_file_path)
    cansat.run_gui()

if __name__ == '__main__':
    main()