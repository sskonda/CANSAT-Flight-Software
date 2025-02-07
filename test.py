'''
24 - 25 CANSAT GUI Simulation and Testing Code
Team Lead: Sanat Konda
Author: Sanat Konda

Purpose: 
This code is designed to simulate sensor data and provide a testing environment for the CANSAT GUI. It allows the user to test and modify the GUI functionality without relying on a live connection to the CANSAT hardware or the radio system. By generating test data in a CSV format, the code provides a controlled environment for validating the GUI's behavior and ensuring it works as expected during development.

Code Overview:
- The code generates a test CSV file containing simulated sensor data (Altitude, Airspeed, Temperature, Battery Voltage, Latitude, Longitude) over time.
- The data is read from the CSV file and used to plot various sensor readings in real-time on the GUI.
- The plots include Altitude vs Time, Airspeed vs Time, Temperature vs Time, Battery Voltage vs Time, Latitude vs Time, and Longitude vs Time.
- The GUI displays the plots alongside live data for the current battery, latitude, and longitude values.
- Upon closing the GUI, the test CSV file is automatically deleted to maintain a clean environment.
'''


import pandas as pd
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import os
import math

# Constants for simulation
g = 9.81  # Gravitational acceleration in m/s^2
terminal_velocity = 50  # Estimated terminal velocity for a 1.5kg satellite in m/s (typical for small objects in free fall)
temperature_at_sea_level = 25  # Average temperature at sea level in Celsius
temperature_lapse_rate = 0.0065  # Temperature decrease per meter of ascent (in Celsius per meter)
pressure_at_sea_level = 101325 # Pressure in Pascals at sea level
M = 0.0289644 # Molar mass of Earth's air in kg/mol
R = 8.314 # Universal gas constant in J/(mol*K)



# Generate test CSV data if not already present
def generate_test_csv(csv_path):
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as f:
            f.write("Time,Altitude,Airspeed,Temperature,Battery,Latitude,Longitude,Pressure\n")
            initial_altitude = 800  # Start at 800 meters
            for t in range(100):
                # Altitude decreases over time (linear fall for simplicity, could be adjusted for more realism)
                altitude = max(0, initial_altitude - (initial_altitude / 100) * t)

                # Airspeed increases until terminal velocity is reached
                airspeed = min(terminal_velocity, g * t)

                # Temperature decreases with altitude (simplified model)
                temperature = temperature_at_sea_level - temperature_lapse_rate * altitude

                # Battery decreases slowly (linear model for simplicity)
                battery = max(3.5, 4.2 - 0.007 * t)  # Starts at 4.2V and decreases by 0.007V per second

                # Random Latitude and Longitude within a reasonable range (simulation purposes)
                latitude = random.uniform(-90, 90)
                longitude = random.uniform(-180, 180)

                pressure = pressure_at_sea_level*math.exp(-M*g*altitude / (R*(temperature+273.15)))
                

                f.write(f"{t},{altitude:.2f},{airspeed:.2f},{temperature:.2f},{battery:.2f},{latitude:.6f},{longitude:.6f},{pressure:.2f}\n")

# def generate_test_csv(csv_path):
#     if not os.path.exists(csv_path):
#         with open(csv_path, 'w') as f:
#             f.write("Time,Altitude,Airspeed,Temperature,Battery,Latitude,Longitude\n")
#             for t in range(100):
#                 f.write(f"{t},{random.randint(100, 1000)},{random.uniform(0, 30):.2f},"
#                         f"{random.uniform(-10, 40):.2f},{random.uniform(3.5, 4.2):.2f},"
#                         f"{random.uniform(-90, 90):.6f},{random.uniform(-180, 180):.6f}\n")

# Function to draw matplotlib graphs onto a PySimpleGUI canvas
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# GUI layout and main logic
def main(csv_file_path):
    # Generate test data
    generate_test_csv(csv_file_path)

    # Read CSV data
    df = pd.read_csv(csv_file_path)

    # Create Matplotlib figures for graphs
    fig_alt, ax_alt = plt.subplots(figsize=(4, 3))
    ax_alt.plot(df['Time'], df['Altitude'], label="Altitude (m)", color="blue")
    ax_alt.set_title("Altitude vs Time")
    ax_alt.set_xlabel("Time (s)")
    ax_alt.set_ylabel("Altitude (m)")
    ax_alt.legend()
    fig_alt.tight_layout()

    fig_aspd, ax_aspd = plt.subplots(figsize=(4, 3))
    ax_aspd.plot(df['Time'], df['Airspeed'], label="Airspeed (m/s)", color="green")
    ax_aspd.set_title("Airspeed vs Time")
    ax_aspd.set_xlabel("Time (s)")
    ax_aspd.set_ylabel("Airspeed (m/s)")
    ax_aspd.legend()
    fig_aspd.tight_layout()

    fig_temp, ax_temp = plt.subplots(figsize=(4, 3))
    ax_temp.plot(df['Time'], df['Temperature'], label="Temperature (°C)", color="red")
    ax_temp.set_title("Temperature vs Time")
    ax_temp.set_xlabel("Time (s)")
    ax_temp.set_ylabel("Temperature (°C)")
    ax_temp.legend()
    fig_temp.tight_layout()

    fig_batt, ax_batt = plt.subplots(figsize=(4, 3))
    ax_batt.plot(df['Time'], df['Battery'], label="Battery Voltage (V)", color="orange")
    ax_batt.set_title("Battery Voltage vs Time")
    ax_batt.set_xlabel("Time (s)")
    ax_batt.set_ylabel("Battery Voltage (V)")
    ax_batt.legend()
    fig_batt.tight_layout()

    fig_lat, ax_lat = plt.subplots(figsize=(4, 3))
    ax_lat.plot(df['Time'], df['Latitude'], label="Latitude", color="purple")
    ax_lat.set_title("Latitude vs Time")
    ax_lat.set_xlabel("Time (s)")
    ax_lat.set_ylabel("Latitude")
    ax_lat.legend()
    fig_lat.tight_layout()

    fig_lon, ax_lon = plt.subplots(figsize=(4, 3))
    ax_lon.plot(df['Time'], df['Longitude'], label="Longitude", color="brown")
    ax_lon.set_title("Longitude vs Time")
    ax_lon.set_xlabel("Time (s)")
    ax_lon.set_ylabel("Longitude")
    ax_lon.legend()
    fig_lon.tight_layout()

    fig_pres, ax_pres = plt.subplots(figsize=(4, 3))
    ax_pres.plot(df['Time'], df['Pressure'], label="Pressure", color="indigo")
    ax_pres.set_title("Pressure vs Time")
    ax_pres.set_xlabel("Time (s)")
    ax_pres.set_ylabel("Pressure")
    ax_pres.legend()
    fig_pres.tight_layout()


    # GUI layout
    graph_column = sg.Column([
        [sg.Canvas(key='-ALT_CANVAS-', size=(400, 250)), sg.Canvas(key='-ASP_CANVAS-', size=(400, 250)),
          sg.Canvas(key='-TEMP_CANVAS-', size=(400, 250))], 
        [sg.Canvas(key='-BATT_CANVAS-', size=(400, 250)), sg.Canvas(key='-LAT_CANVAS-', size=(400, 250)),
         sg.Canvas(key='-LON_CANVAS-', size=(400, 250))],
        [sg.Canvas(key='-PRES_CANVAS-', size=(400, 250))],
        [sg.Text("Battery Voltage:", size=(15, 1)), sg.Text(f"{df['Battery'].iloc[-1]:.2f} V", key='-BATTERY-')],
        [sg.Text("Latitude:", size=(15, 1)), sg.Text(f"{df['Latitude'].iloc[-1]:.6f}", key='-LATITUDE-')],
        [sg.Text("Longitude:", size=(15, 1)), sg.Text(f"{df['Longitude'].iloc[-1]:.6f}", key='-LONGITUDE-')],
        [sg.Text("Pressure:", size=(15, 1)), sg.Text(f"{df['Pressure'].iloc[-1]:.6f}", key='-PRESSURE-')],
        [sg.Button("Exit", size=(10, 1))]
    ], 
    scrollable = True,
    vertical_scroll_only = True,
    size = (3000,2400)
    )

    layout = [
        [sg.Text("CanSat Test GUI", font=('Helvetica', 16), justification='center', expand_x=True)],
        [sg.Column([[graph_column]], size=(3000,2400), scrollable=True, vertical_scroll_only=True)]
    ]

    # Create the PySimpleGUI window
    window = sg.Window("CanSat GUI", layout, resizable=True, finalize=True)

    # Embed Matplotlib figures in the PySimpleGUI window
    draw_figure(window['-ALT_CANVAS-'].Widget, fig_alt)
    draw_figure(window['-ASP_CANVAS-'].Widget, fig_aspd)
    draw_figure(window['-TEMP_CANVAS-'].Widget, fig_temp)
    draw_figure(window['-BATT_CANVAS-'].Widget, fig_batt)
    draw_figure(window['-LAT_CANVAS-'].Widget, fig_lat)
    draw_figure(window['-LON_CANVAS-'].Widget, fig_lon)
    draw_figure(window['-PRES_CANVAS-'].Widget, fig_pres)

    # Event loop
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        # Update data dynamically (if real-time functionality is added later)
        window['-BATTERY-'].update(f"{df['Battery'].iloc[-1]:.2f} V")
        window['-LATITUDE-'].update(f"{df['Latitude'].iloc[-1]:.6f}")
        window['-LONGITUDE-'].update(f"{df['Longitude'].iloc[-1]:.6f}")

    window.close()
    # Delete the test CSV file
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

# Run the program
if __name__ == "__main__":
    test_csv_path = "test_data.csv"
    main(test_csv_path)
