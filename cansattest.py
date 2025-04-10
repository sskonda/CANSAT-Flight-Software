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

class CanSat:
    def __init__(self, csv_file_path):
        self.data = {
            'TEAM_ID': 3154, 
            'MISSION_TIME': '00:00:00',  # UTC time in hh:mm:ss
            'PACKET_COUNT': 0,  # The total count of transmitted packets since turned on reset to zero by command when the CanSat is installed in the rocket on the launch pad at the beginning of the mission and maintained through processor reset.
            'MODE': 'S',  # 'F' for flight mode and 'S' for simulation mode.
            'STATE': 'U',  # The operation state of the software. (LAUNCH_WAIT, ASCENT, ROCKET_SEPARATION, DESCENT, HS_RELEASE, LANDED, etc).
            'ALTITUDE': 0,  # In units of meters and must be relative to ground level at the launch site.
            'TEMPERATURE': 0,  # In degrees Celsius
            'PRESSURE': 0,  # In Pascals. Air pressure of the sensor used.
            'VOLTAGE': 0,  # Voltage of the CanSat power bus
            'GYRO_R': 0,  # Gyroscope Roll in degrees/second
            'GYRO_P': 0,  # Gyroscope Pitch in degrees/second
            'GYRO_Y': 0,  # Gyroscope Yaw in degrees/second
            'ACCEL_R': 0,  # Accelerometer Roll in m/s²
            'ACCEL_P': 0,  # Accelerometer Pitch in m/s²
            'ACCEL_Y': 0,  # Accelerometer Yaw in m/s²
            'MAG_R': 0,  # Magnetometer Roll in µT
            'MAG_P': 0,  # Magnetometer Pitch in µT
            'MAG_Y': 0,  # Magnetometer Yaw in µT
            'AUTO_GYRO_ROTATION_RATE': 0,  # Auto-Gyro Rotation Rate
            'GPS_TIME': '00:00:00',  # In UTC. Time from the GPS receiver.
            'GPS_ALTITUDE': 0,  # In meters. The altitude from the GPS receiver above mean sea level.
            'GPS_LATITUDE': 0,  # In degrees North. The latitude from the GPS receiver.
            'GPS_LONGITUDE': 0,  # In degrees West. The longitude from the GPS receiver.
            'GPS_SATS': 0,  # Number of GPS satellites being tracked by the GPS receiver.
            'CMD_ECHO': "CXON"  # Text of the last command received and processed by the CanSat.
        }
        self.csv_file_path = csv_file_path

        # Check if the file exists and is not empty
        import os
        if not os.path.exists(self.csv_file_path):
            print(f"CSV file not found: {self.csv_file_path}")
            return
        if os.path.getsize(self.csv_file_path) == 0:
            print("CSV file is empty.")
            return

        # Attempt to read the CSV file
        try:
            self.df = pd.read_csv(self.csv_file_path)
        except pd.errors.EmptyDataError:
            print("CSV file is empty or improperly formatted.")
            self.df = None
        except FileNotFoundError:
            print(f"CSV file not found: {self.csv_file_path}")
            self.df = None
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            self.df = None

        self.graph_canvases = {}
        self.layout = self.create_gui_layout()
        self.window = sg.Window('CanSat Dashboard', self.layout, background_color=PRIMARY_COLOR, finalize=True)
        self.window.Maximize()
        self.window.TKroot.resizable(True, True)
        self.window.move(0, 0)

        if self.df is None or len(self.df) < 1:
            self.internalpc = 1
        else:
            self.internalpc = len(self.df)

        self.simulation_mode = True  # Simulation mode flag, set to true for testing purposes

        # Initializes graphs
        fig_size = (self.window.size[0] / 350, self.window.size[1] / 250)  # Change the numerator in order to change the size of the graphs.
        self.graphs = {
            'altitude': plt.subplots(figsize=(fig_size)),
            'auto_gyro_rotation_rate': plt.subplots(figsize=(fig_size)),  # Auto-Gyro Rotation Rate
            'temperature': plt.subplots(figsize=(fig_size)),
            'pressure': plt.subplots(figsize=(fig_size)),
            'voltage': plt.subplots(figsize=(fig_size)),
            'gps_altitude': plt.subplots(figsize=(fig_size)),
            'gps_latitude': plt.subplots(figsize=(fig_size)),
            'gps_longitude': plt.subplots(figsize=(fig_size)),
            'gyro_combined': plt.subplots(figsize=(fig_size)),  # Combined Gyroscope graph
            'accel_combined': plt.subplots(figsize=(fig_size)),  # Combined Accelerometer graph
            'mag_combined': plt.subplots(figsize=(fig_size))  # Combined Magnetometer graph
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
            sg.Text('Mode: ' + self.data['MODE'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='MODE', pad=(0, 0)),
            sg.Text('GPS Time: ' + self.data['GPS_TIME'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(25, 1), justification='left', key='GPS_TIME', pad=(0, 0)),
            sg.Text('Software State: ' + self.data['STATE'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='STATE', pad=(0, 0))
        ]

    def create_third_row(self):
        return [
            sg.Text('Packet Count: ' + str(self.data['PACKET_COUNT']), font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='PC1', pad=(0, 0)),
            sg.Text('GPS Sat: ' + str(self.data['GPS_SATS']), font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(25, 1), justification='left', key='GPS_SATS', pad=(0,0)),
            sg.Text('CMD Echo: ' + self.data['CMD_ECHO'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='left', key='CMD_ECHO', pad=(0,0))
        ]

    def create_fourth_row(self):
        graph_size = (300, 300)  # Adjust size as needed
        return [
            sg.Canvas(key='graph_canvas_altitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_auto_gyro_rotation_rate', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
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
            sg.Canvas(key='graph_canvas_gyro_combined', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_accel_combined', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0)),
            sg.Canvas(key='graph_canvas_mag_combined', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(0,0))
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
        if len(data_one_col) > 7:
            last_rows = pd.read_csv(self.csv_file_path, header=None, names=[
                "TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE", "TEMPERATURE", "PRESSURE", "VOLTAGE",
                "GYRO_R", "GYRO_P", "GYRO_Y", "ACCEL_R", "ACCEL_P", "ACCEL_Y", "MAG_R", "MAG_P", "MAG_Y",
                "AUTO_GYRO_ROTATION_RATE", "GPS_TIME", "GPS_ALTITUDE", "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_SATS", "CMD_ECHO"
            ], skiprows=len(data_one_col) - 7)
        else:
            last_rows = pd.read_csv(self.csv_file_path, header=None, names=[
                "TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE", "TEMPERATURE", "PRESSURE", "VOLTAGE",
                "GYRO_R", "GYRO_P", "GYRO_Y", "ACCEL_R", "ACCEL_P", "ACCEL_Y", "MAG_R", "MAG_P", "MAG_Y",
                "AUTO_GYRO_ROTATION_RATE", "GPS_TIME", "GPS_ALTITUDE", "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_SATS", "CMD_ECHO"
            ], skiprows=1)

        graph_data = {
            'time': last_rows['MISSION_TIME'].tolist(),
            'altitude': last_rows['ALTITUDE'].tolist(),
            'auto_gyro_rotation_rate': last_rows['AUTO_GYRO_ROTATION_RATE'].tolist(),
            'temperature': last_rows['TEMPERATURE'].tolist(),
            'pressure': last_rows['PRESSURE'].tolist(),
            'voltage': last_rows['VOLTAGE'].tolist(),
            'gps_altitude': last_rows['GPS_ALTITUDE'].tolist(),
            'gps_latitude': last_rows['GPS_LATITUDE'].tolist(),
            'gps_longitude': last_rows['GPS_LONGITUDE'].tolist(),
            'gyro_r': last_rows['GYRO_R'].tolist(),
            'gyro_p': last_rows['GYRO_P'].tolist(),
            'gyro_y': last_rows['GYRO_Y'].tolist(),
            'accel_r': last_rows['ACCEL_R'].tolist(),
            'accel_p': last_rows['ACCEL_P'].tolist(),
            'accel_y': last_rows['ACCEL_Y'].tolist(),
            'mag_r': last_rows['MAG_R'].tolist(),
            'mag_p': last_rows['MAG_P'].tolist(),
            'mag_y': last_rows['MAG_Y'].tolist()
        }
        return graph_data
    
    # Updates all the graphs on the GUI
    def update_graphs(self, new_data):
        self.data["MISSION_TIME"] = str(new_data["time"][-1])
        self.data["ALTITUDE"] = str(new_data["altitude"][-1])
        self.data["AUTO_GYRO_ROTATION_RATE"] = str(new_data["auto_gyro_rotation_rate"][-1])

        for key, (fig, ax) in self.graphs.items():
            ax.clear()
            if key == 'gyro_combined':
                ax.plot(new_data['time'], new_data['gyro_r'], label='Roll', color='red')
                ax.plot(new_data['time'], new_data['gyro_p'], label='Pitch', color='green')
                ax.plot(new_data['time'], new_data['gyro_y'], label='Yaw', color='blue')
                ax.set_title('Gyroscope (Roll, Pitch, Yaw) vs Time', color=GRAPH_TEXT_COLOR, fontweight='bold')
                ax.set_xlabel('Time (s)', color=GRAPH_TEXT_COLOR)
                ax.set_ylabel('Degrees/Second', color=GRAPH_TEXT_COLOR)
                ax.legend()
            elif key == 'accel_combined':
                ax.plot(new_data['time'], new_data['accel_r'], label='Roll', color='red')
                ax.plot(new_data['time'], new_data['accel_p'], label='Pitch', color='green')
                ax.plot(new_data['time'], new_data['accel_y'], label='Yaw', color='blue')
                ax.set_title('Accelerometer (Roll, Pitch, Yaw) vs Time', color=GRAPH_TEXT_COLOR, fontweight='bold')
                ax.set_xlabel('Time (s)', color=GRAPH_TEXT_COLOR)
                ax.set_ylabel('Acceleration (m/s²)', color=GRAPH_TEXT_COLOR)
                ax.legend()
            elif key == 'mag_combined':
                ax.plot(new_data['time'], new_data['mag_r'], label='Roll', color='red')
                ax.plot(new_data['time'], new_data['mag_p'], label='Pitch', color='green')
                ax.plot(new_data['time'], new_data['mag_y'], label='Yaw', color='blue')
                ax.set_title('Magnetometer (Roll, Pitch, Yaw) vs Time', color=GRAPH_TEXT_COLOR, fontweight='bold')
                ax.set_xlabel('Time (s)', color=GRAPH_TEXT_COLOR)
                ax.set_ylabel('Magnetic Field (µT)', color=GRAPH_TEXT_COLOR)
                ax.legend()
            elif key in new_data and 'time' in new_data and len(new_data[key]) == len(new_data['time']):
                ax.plot(new_data['time'], new_data[key], color='black')
                ax.set_title(f'{key.replace("_", " ").title()} vs Time', color=GRAPH_TEXT_COLOR, fontweight='bold')
                ax.set_xlabel('Time (s)', color=GRAPH_TEXT_COLOR)
                ax.set_ylabel(f'{key.replace("_", " ").title()}', color=GRAPH_TEXT_COLOR)
            self.graph_canvases[key][0].draw()
    
    # Updates any text-based data at the top of the GUI
    def update_header_elements(self):
        self.window['TEAM_ID'].update('Team ID: ' + str(self.data['TEAM_ID']))
        self.window['MISSION_TIME'].update('Mission Time: ' + self.data['MISSION_TIME'])
        self.window['PC1'].update('Packet Count: ' + str(self.data['PACKET_COUNT']))
        self.window['MODE'].update('Mode: ' + self.data['MODE'])
        self.window['STATE'].update('Software State: ' + self.data['STATE'])
        self.window['GPS_SATS'].update('GPS Sat: ' + str(self.data['GPS_SATS']))
        self.window['GPS_TIME'].update('GPS Time: ' + self.data['GPS_TIME'])
        self.window['CMD_ECHO'].update('CMD Echo: ' + self.data['CMD_ECHO'])


    def run_gui(self):
        # Check if the file exists and is not empty
        import os
        if not os.path.exists(self.csv_file_path):
            print(f"CSV file not found: {self.csv_file_path}")
            return
        if os.path.getsize(self.csv_file_path) == 0:
            print("CSV file is empty.")
            return

        # Create the initial CSV file and write the header if it doesn't exist
        try:
            with open(self.csv_file_path, 'x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE", "TEMPERATURE", "PRESSURE", "VOLTAGE",
                    "GYRO_R", "GYRO_P", "GYRO_Y", "ACCEL_R", "ACCEL_P", "ACCEL_Y", "MAG_R", "MAG_P", "MAG_Y",
                    "AUTO_GYRO_ROTATION_RATE", "GPS_TIME", "GPS_ALTITUDE", "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_SATS", "CMD_ECHO"
                ])
        except FileExistsError:
            pass  # File already exists, no need to create it

        ser = None
        if not self.simulation_mode:
            # Initialize the serial port for radio communication
            ser = serial.Serial()
            ser.baudrate = 19200
            ser.port = 'COM5'
            ser.open()
            print(ser)

        while True:
            if self.simulation_mode:
                # Read the last row of the CSV file to generate simulated data
                try:
                    df = pd.read_csv(self.csv_file_path, skiprows=1)
                    if df.empty:
                        print("CSV file is empty. No data to parse.")
                        continue
                except pd.errors.EmptyDataError:
                    print("CSV file is empty or improperly formatted.")
                    continue
                except FileNotFoundError:
                    print(f"CSV file not found: {self.csv_file_path}")
                    continue
                except Exception as e:
                    print(f"Error reading CSV file: {e}")
                    continue

                if not df.empty:
                    last_row = df.iloc[-1]
                    simulated_data = [
                        last_row["TEAM_ID"], time.strftime('%H:%M:%S'), last_row["PACKET_COUNT"] + 1, 'S', 'SIMULATION',
                        last_row["ALTITUDE"], last_row["TEMPERATURE"], last_row["PRESSURE"], last_row["VOLTAGE"],
                        last_row["GYRO_R"], last_row["GYRO_P"], last_row["GYRO_Y"],
                        last_row["ACCEL_R"], last_row["ACCEL_P"], last_row["ACCEL_Y"],
                        last_row["MAG_R"], last_row["MAG_P"], last_row["MAG_Y"],
                        last_row["AUTO_GYRO_ROTATION_RATE"], time.strftime('%H:%M:%S'),
                        last_row["GPS_ALTITUDE"], last_row["GPS_LATITUDE"], last_row["GPS_LONGITUDE"],
                        last_row["GPS_SATS"], 'SIM'
                    ]
                else:
                    # Default simulated data if the CSV is empty
                    simulated_data = [
                        self.data['TEAM_ID'], time.strftime('%H:%M:%S'), self.data['PACKET_COUNT'], 'S', 'SIMULATION',
                        1000, 20.5, 101325, 4.2,  # Altitude, Temperature, Pressure, Voltage
                        0.5, -0.3, 0.1,  # Gyro (Roll, Pitch, Yaw)
                        0.02, -0.01, 0.03,  # Accelerometer (Roll, Pitch, Yaw)
                        30, -15, 45,  # Magnetometer (Roll, Pitch, Yaw)
                        5.0,  # Auto-Gyro Rotation Rate
                        time.strftime('%H:%M:%S'), 500, 37.7749, -122.4194, 8, 'SIM'
                    ]

                # Write the simulated data to the CSV file
                with open(self.csv_file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(simulated_data)
                self.data['PACKET_COUNT'] += 1

            else:
                # Real hardware mode: check for new incoming messages from the radio
                with open(self.csv_file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    if ser.in_waiting > 0:
                        try:
                            xbee_message = ser.readline().decode('utf-8')
                            print(xbee_message)
                            writer.writerow(xbee_message.strip().split(','))
                        except:
                            print("Error reading in packet.")

            # Read GUI events
            start_time = time.perf_counter()
            event, values = self.window.read(timeout=50)

            if event == sg.WIN_CLOSED or event == '':
                break

            if event == 'Sim_Mode':
                self.simulation_mode = not self.simulation_mode
                print(f"Simulation Mode {'Enabled' if self.simulation_mode else 'Disabled'}")
                if self.simulation_mode and ser:
                    ser.close()

            if event == "Send" and not self.simulation_mode:
                print("Send Button Pressed")
                print(values[0])
                time.sleep(1)
                ser.write(bytes(values[0], 'utf-8'))

            # Read and update graphs with new data
            try:
                data_one_col = pd.read_csv(self.csv_file_path, usecols=["PACKET_COUNT"])
            except:
                print("CAN'T READ")
                continue

            if len(data_one_col) > self.internalpc:
                self.internalpc = len(data_one_col)

                # Reads the latest row of data
                new_data = self.read_latest_csv_data(data_one_col)
                new_data_time = time.perf_counter()
                duration = round(new_data_time - start_time, 5)

                # Update header elements
                self.update_graphs(new_data)
                update_graphs_time = time.perf_counter()
                duration = round(update_graphs_time - new_data_time, 5)

                # Update header elements
                self.update_header_elements()
                end_time = time.perf_counter()
                duration = round(end_time - start_time, 5)

        self.window.close()

def main():
    # Use SimCSV.csv if you are able to run the python skit alongside the VSCode
    # Else use Sample_Flight.csv
    csv_file_path = "SimCSV.csv" # Have it depend on the mode. I think we might have to create a csv file here too?
    cansat = CanSat(csv_file_path)
    cansat.run_gui()

if __name__ == '__main__':
    main()