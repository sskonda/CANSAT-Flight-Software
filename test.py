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

# Generate test CSV data if not already present
def generate_test_csv(csv_path):
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as f:
            f.write("Time,Altitude,Airspeed,Temperature,Battery,Latitude,Longitude\n")
            for t in range(100):
                f.write(f"{t},{random.randint(100, 1000)},{random.uniform(0, 30):.2f},"
                        f"{random.uniform(-10, 40):.2f},{random.uniform(3.5, 4.2):.2f},"
                        f"{random.uniform(-90, 90):.6f},{random.uniform(-180, 180):.6f}\n")

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
    fig_alt, ax_alt = plt.subplots(figsize=(5, 3))
    ax_alt.plot(df['Time'], df['Altitude'], label="Altitude (m)", color="blue")
    ax_alt.set_title("Altitude vs Time")
    ax_alt.set_xlabel("Time (s)")
    ax_alt.set_ylabel("Altitude (m)")
    ax_alt.legend()

    fig_aspd, ax_aspd = plt.subplots(figsize=(5, 3))
    ax_aspd.plot(df['Time'], df['Airspeed'], label="Airspeed (m/s)", color="green")
    ax_aspd.set_title("Airspeed vs Time")
    ax_aspd.set_xlabel("Time (s)")
    ax_aspd.set_ylabel("Airspeed (m/s)")
    ax_aspd.legend()

    fig_temp, ax_temp = plt.subplots(figsize=(5, 3))
    ax_temp.plot(df['Time'], df['Temperature'], label="Temperature (°C)", color="red")
    ax_temp.set_title("Temperature vs Time")
    ax_temp.set_xlabel("Time (s)")
    ax_temp.set_ylabel("Temperature (°C)")
    ax_temp.legend()

    fig_batt, ax_batt = plt.subplots(figsize=(5, 3))
    ax_batt.plot(df['Time'], df['Battery'], label="Battery Voltage (V)", color="orange")
    ax_batt.set_title("Battery Voltage vs Time")
    ax_batt.set_xlabel("Time (s)")
    ax_batt.set_ylabel("Battery Voltage (V)")
    ax_batt.legend()

    fig_lat, ax_lat = plt.subplots(figsize=(5, 3))
    ax_lat.plot(df['Time'], df['Latitude'], label="Latitude", color="purple")
    ax_lat.set_title("Latitude vs Time")
    ax_lat.set_xlabel("Time (s)")
    ax_lat.set_ylabel("Latitude")
    ax_lat.legend()

    fig_lon, ax_lon = plt.subplots(figsize=(5, 3))
    ax_lon.plot(df['Time'], df['Longitude'], label="Longitude", color="brown")
    ax_lon.set_title("Longitude vs Time")
    ax_lon.set_xlabel("Time (s)")
    ax_lon.set_ylabel("Longitude")
    ax_lon.legend()

    # GUI layout
    layout = [
        [sg.Text("CanSat Test GUI", font=('Helvetica', 16), justification='center', expand_x=True)],
        [sg.Canvas(key='-ALT_CANVAS-'), sg.Canvas(key='-ASP_CANVAS-')],
        [sg.Canvas(key='-TEMP_CANVAS-'), sg.Canvas(key='-BATT_CANVAS-')],
        [sg.Canvas(key='-LAT_CANVAS-'), sg.Canvas(key='-LON_CANVAS-')],
        [sg.Text("Battery Voltage:", size=(15, 1)), sg.Text(f"{df['Battery'].iloc[-1]:.2f} V", key='-BATTERY-')],
        [sg.Text("Latitude:", size=(15, 1)), sg.Text(f"{df['Latitude'].iloc[-1]:.6f}", key='-LATITUDE-')],
        [sg.Text("Longitude:", size=(15, 1)), sg.Text(f"{df['Longitude'].iloc[-1]:.6f}", key='-LONGITUDE-')],
        [sg.Button("Exit", size=(10, 1))]
    ]

    # Create the PySimpleGUI window
    window = sg.Window("CanSat GUI", layout, finalize=True)

    # Embed Matplotlib figures in the PySimpleGUI window
    draw_figure(window['-ALT_CANVAS-'].Widget, fig_alt)
    draw_figure(window['-ASP_CANVAS-'].Widget, fig_aspd)
    draw_figure(window['-TEMP_CANVAS-'].Widget, fig_temp)
    draw_figure(window['-BATT_CANVAS-'].Widget, fig_batt)
    draw_figure(window['-LAT_CANVAS-'].Widget, fig_lat)
    draw_figure(window['-LON_CANVAS-'].Widget, fig_lon)

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
