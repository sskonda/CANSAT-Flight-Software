# CANSAT Flight Software

This repository contains the flight software for our CANSAT project. The software is responsible for collecting and transmitting sensor data, managing telemetry, and executing descent and separation procedures. This project is developed as part of our CANSAT competition entry, where we design a payload and container system that separates mid-flight, with the payload descending via an auto-gyro system and the container using a parachute.

## Project Overview

The flight software enables reliable telemetry, data collection, and control functionalities required by the CANSAT competition. Key responsibilities include:

- **Sensor Data Collection**: Readings from GPS, temperature, altitude, battery status, and other sensors.
- **Telemetry**: Transmission of data packets to the ground station at a 1 Hz rate.
- **Separation Control**: Manages the container and payload separation mid-flight.
- **Descent Management**: Supports auto-gyro descent for the payload and parachute descent for the container.

## Overview of Flight Software

This flight software for the CANSAT project is structured to handle both data processing and telemetry visualization, integrating with Python libraries such as Pandas, PySimpleGUI, and Matplotlib. Here’s a detailed look at how it operates:

1. **Data Initialization**: 
   - The main `CanSat` class holds a dictionary, `data`, to store key telemetry information such as altitude, temperature, GPS data, and battery status. Each parameter has a placeholder value that is updated with live telemetry data as it is read.

2. **Data Loading**:
   - On startup, the software attempts to load historical data from a CSV file (`self.csv_file_path`). If successful, it initializes a Pandas DataFrame (`self.df`) with this data, each row representing a snapshot of the telemetry parameters. This CSV serves as both a record and backup of telemetry data.

3. **GUI Layout**:
   - The GUI is designed with readability and interactivity in mind, displaying telemetry data along with visualizations. The `create_gui_layout` function organizes the GUI’s structure, including sections built by functions like `create_top_banner` and `create_fourth_row`. For graphs, it uses `FigureCanvasTkAgg` to embed Matplotlib graphs into the PySimpleGUI window, providing a clear view of data trends.

4. **Graphs Initialization**:
   - Telemetry parameters, such as altitude and GPS location, are visualized through graphs stored in `self.graphs`. Using Matplotlib, each graph is customized to fit the GUI’s color scheme and to provide real-time updates on telemetry data trends.

5. **CSV Data Reading**:
   - The `read_latest_csv_data` function is responsible for reading the latest row of telemetry data from the CSV file, ensuring that each parameter is updated in near real-time. For testing, the software can be run in a simulation mode, allowing data to be emulated without live inputs. This function reads telemetry columns such as `TEAM_ID`, `MISSION_TIME`, `ALTITUDE`, and `TEMPERATURE`, keeping the displayed data aligned with the most recent readings.

6. **Command Processing**:
   - The GUI includes a top banner with a command dropdown menu, allowing control commands to be sent to the CANSAT system. Commands may include toggling simulation mode, adjusting GPS time, and more, enabling interaction with the CANSAT’s operational state during the mission.

7. **Error Detection and Recovery**:
   - Basic fault-tolerance mechanisms help ensure continuous data transmission to the ground station even if minor communication issues arise.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/cansat-flight-software.git
   cd cansat-flight-software
   ```

2. **Install Python dependencies**:
   Make sure you have Python installed. Then install the required libraries:
   ```bash
   pip install pandas PySimpleGUI matplotlib
   ```

3. **Set up the Raspberry Pi Pico**:
   - Ensure that your Raspberry Pi Pico environment is set up for MicroPython. You can use [Thonny IDE](https://thonny.org/) or follow the [MicroPython documentation](https://docs.micropython.org/en/latest/rp2/quickref.html) for the Raspberry Pi Pico.

4. **Upload the code to the Pico**:
   - Use Thonny IDE or a similar tool to transfer the necessary files to the Raspberry Pi Pico for real-time data collection and transmission.

5. **Run the Software**:
   - Run the main script to start the flight software. It will initialize the GUI, load historical data if available, and begin telemetry transmission.

## Usage

1. **Power up the CANSAT system**.
2. **Verify sensor connections**: Confirm that all sensors are correctly connected and initialized.
3. **Start data transmission**: The flight software will automatically begin sending data packets to the ground station.
4. **Monitor telemetry**: Use the ground station interface to log and visualize incoming telemetry packets.

## Data Packet Format

Data packets are transmitted at a 1 Hz rate with fields formatted as follows:

| Field            | Description                      |
|------------------|----------------------------------|
| TEAM_ID          | Unique ID of the team           |
| MISSION_TIME     | Elapsed time since launch       |
| PACKET_COUNT     | Sequential packet ID            |
| ALTITUDE         | Current altitude of payload     |
| TEMPERATURE      | Ambient temperature             |
| VOLTAGE          | Battery voltage level           |
| GPS_TIME         | GPS-provided timestamp          |
| GPS_LATITUDE     | Latitude                        |
| GPS_LONGITUDE    | Longitude                       |
| GPS_ALTITUDE     | GPS altitude                    |
| PAYLOAD_STATE    | Payload status indicator        |
| CONTAINER_STATE  | Container status indicator      |

## Future Enhancements

- **Advanced Descent Control**: Implementing more precise control of descent mechanisms.
- **Additional Sensor Integration**: Adding new sensors for environmental monitoring.
- **Adaptive Telemetry Rate**: Adjusting transmission rate based on mission phase or altitude.

## Contributing

Contributions to improve the flight software are welcome! Please fork the repository and submit a pull request.
