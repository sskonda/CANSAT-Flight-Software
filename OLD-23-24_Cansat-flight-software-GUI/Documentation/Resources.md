# Resources/Documentation

## Telemetry Team Details

### 3.3.1 Telemetry

Upon power up, the Cansat shall collect the required telemetry at a one (1) Hz sample rate and transmit the telemetry data to the ground station. The ASCII format of the telemetry packets are described below. Each telemetry field is delimited by a comma, and each telemetry packet is terminated by a single carriage return character. No comma (`,`) characters should be part of the data fields -- commas are delimiters only.

### 3.3.1.1 Telemetry Formats

The Cansat telemetry packet format to be transmitted at one (1) Hz is as follows:
TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE, AIR_SPEED, HS_DEPLOYED, PC_DEPLOYED, TEMPERATURE, VOLTAGE, PRESSURE, GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS, TILT_X, TILT_Y, ROT_Z, CMD_ECHO [,,OPTIONAL_DATA]


The telemetry data fields are to be formatted as follows:
1. `TEAM_ID` is the assigned four-digit team identification number. E.g., imaginary team '1000'.
2. `MISSION_TIME` is UTC time in format hh:mm:ss, where hh is hours, mm is minutes, and ss is seconds. E.g., '13:14:02' indicates 1:14:02 PM.
3. `PACKET_COUNT` is the total count of transmitted packets since turn on, which is to be reset to zero by command when the Cansat is installed in the rocket on the launch pad at the beginning of the mission and maintained through processor reset.
4. `MODE` = 'F' for flight mode and 'S' for simulation mode.
5. `STATE` is the operating state of the software (e.g., LAUNCH_WAIT, ASCENT, ROCKET_SEPARATION, DESCENT, HS_RELEASE, LANDED, etc.). Teams may define their own states. This should be a human-readable description as the judges will review it after the launch in the .csv files.
6. `ALTITUDE` is the altitude in units of meters and must be relative to ground level at the launch site. The resolution must be 0.1 meters.
7. `AIR_SPEED` is the airspeed in meters per second measured with the pitot tube during both ascent and descent.
8. `HS_DEPLOYED` = 'P' indicates the heat shield is deployed, 'N' otherwise.
9. `PC_DEPLOYED` = 'C' indicates the parachute is deployed (at 100 m), 'N' otherwise.
10. `TEMPERATURE` is the temperature in degrees Celsius with a resolution of 0.1 degrees.
11. `PRESSURE` is the air pressure of the sensor used. Value must be in kPa with a resolution of 0.1 kPa.
12. `VOLTAGE` is the voltage of the Cansat power bus with a resolution of 0.1 volts.
13. `GPS_TIME` is the time from the GPS receiver. The time must be reported in UTC and have a resolution of a second.
14. `GPS_ALTITUDE` is the altitude from the GPS receiver in meters above mean sea level with a resolution of 0.1 meters.
15. `GPS_LATITUDE` is the latitude from the GPS receiver in decimal degrees with a resolution of 0.0001 degrees North.
16. `GPS_LONGITUDE` is the longitude from the GPS receiver in decimal degrees with a resolution of 0.0001 degrees West.
17. `GPS_SATS` is the number of GPS satellites being tracked by the GPS receiver. This must be an integer.
18. `TILT_X`, `TILT_Y` are the angles of the Cansat X and Y axes in degrees, with a resolution of 0.01 degrees, where zero degrees is defined as when the axes are perpendicular to the Z axis which is defined as towards the center of gravity of the Earth.
19. `ROT_Z` is the rotation rate of the Cansat in degrees per second with a resolution of 0.1 degrees per second.
20. `CMD_ECHO` is the text of the last command received and processed by the Cansat. For example, CXON or SP101325. See the command section for details of command formats. Do not include commas characters.
21. `[,,OPTIONAL_DATA]` are zero or more additional fields the team considers important following two commas, which indicate a blank field. This data must follow the same format rules (including the use of comma characters ',') to facilitate review of the CSV files by the judges after the mission.

### 3.3.1.2 Telemetry Data Files

The received telemetry for the entire mission shall be saved on the ground station computer as comma-separated value (.csv) files that will be examined by the competition judges in Excel. The CSV format should be the same as used by export from Excel. Teams shall provide the CSV file to the judges immediately after the launch operations via USB drive.

The CSV files shall include a header specifying the name of each field/column of data in the file. The telemetry data files shall be named as follows:
- `Flight_<TEAM_ID>.csv` where the team_id is the four-digit team id number. For example: `Flight_1000.csv` is the required file name for imaginary team 1000.

The ground software shall produce the files, with the correct name, easily from the ground system user interface, and save them to the provided USB memory stick, which is to be given to judges before leaving the launch area.

### 3.3.2.3 On-board Telemetry Storage

It is suggested that teams make use of onboard data storage as backup in case of radio failure. Only the transmitted telemetry is examined and scored on flight day; however, the backup data can be used when preparing the Post Flight Review presentation.

## 3.3.2 Commands

The payload shall receive and process the following commands from the Ground Station:

- CX - Payload Telemetry On/Off Command
CMD,<TEAM_ID>,CX,<ON_OFF>

Where:
- CMD and CX are static text.
- <TEAM ID> is the assigned team identification.
- <ON_OFF> is the string 'ON' to activate the payload telemetry transmissions and 'OFF' to turn off the transmissions.
Example: The command `CMD,1000,CX,ON` activates payload telemetry transmission, assuming the team id is 1000.

- ST - Set Time
CMD,<TEAM_ID>,ST,<UTC_TIME>|GPS

Where:
- CMD and ST are static text.
- <TEAM ID> is the assigned team identification.
- <UTC_TIME>|GPS is UTC time in the format hh:mm:ss or 'GPS' which sets the flight software time to the current time read from the GPS module.
Example: The command `CMD,1000,ST,13:35:59` sets the mission time to the value given, and the command `CMD,1000,ST,GPS` sets the time to the current GPS time. Note: It is recommended that the time be set directly from the Ground System time, in UTC, or from the GPS rather than being typed into the command manually.

- SIM - Simulation Mode Control Command
CMD,<TEAM_ID>,SIM,<MODE>

Where:
1. CMD and SIM are static text.
2. `<TEAM_ID>` is the assigned team identification.
3. `<MODE>` is the string 'ENABLE' to enable the simulation mode, 'ACTIVATE' to activate the simulation mode, or 'DISABLE' which both disables and deactivates the simulation mode.
Example: Both the `CMD,1000,SIM,ENABLE` and `CMD,1000,SIM,ACTIVATE` commands are required to begin simulation mode.
Note: It is advised that care be taken to not allow mixing of simulated and actual barometric altitude data. This caused at least one failure in the recent launches.

- SIMP - Simulated Pressure Data (to be used in Simulation Mode only)
CMD,<TEAM ID>,SIMP,<PRESSURE>

Where:
1. CMD and SIMP are static text.
2. `<TEAM_ID>` is the assigned team identification.
3. `<PRESSURE>` is the simulated atmospheric pressure data in units of pascals with a resolution of one Pascal.
Example: `CMD,1000,SIMP,101325` provides a simulated pressure reading to the payload (101325 Pascals = approximately sea level). Note: this command is to be used only in simulation mode.
Note: Pressure values in the SIMP profile are not calibrated to be relative to the launch site altitude, but are absolute altitudes above sea level.

- CAL - Calibrate Altitude to Zero
CMD,<TEAM ID>,CAL

The CAL command is to be sent when the Cansat is installed on the launch pad and causes the flight software to calibrate the telemetered altitude to 0 meters.
Note: This command also can be used by the flight software to reset and enable processor reset recovery algorithms. (Note: more than three teams failed to complete the mission last year because of processor resets during the launch; so, be prepared.)

- BCN - Control Audio Beacon
CMD,<TEAM ID>,BCN,ON|OFF

Where:
1. CMD and BCN are static text.
2. `<TEAM_ID>` is the assigned team identification.
3. `<ON|OFF>` are static strings 'ON' or 'OFF' that control the audio beacon.
The BCN command allows the audio beacon, which is normally activated only upon landing, to be activated and deactivated for testing and inspection and the flight readiness review.

- OPTIONAL - Optional Commands
The team may implement additional commands that are useful for testing or controlling the Cansat. For example: it is a good idea to implement commands to activate mechanisms and the audible beacon for testing and demonstration purposes.
Note: commanding during flight is a risky operation as radio links and precise timing are unreliable; so, autonomous Cansat flight software operation should be the primary mechanism for mission success.

## 3.3.3 Simulation Mode

The Cansat payload shall operate in two modes:
- FLIGHT mode where the Cansat operates as described in the Mission Overview section using actual sensor data, and
- SIMULATION mode where the Cansat receives simulated barometric pressure values from the Ground Station via SIMP commands and substitutes those values for the actual pressure sensor reading for calculation of altitude and for use by the flight software logic.


## Agile Workflow using Continuous Delivery/Integration Techniques

To understand the development flow for making changes to the project, refer to the following link. It describes the model you will follow for continuous development:

- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

## Useful Links for Understanding Project Dependencies
- [Basic NumPy Tutorial Guide - This is all we really need to know](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Matplotlib 3D Plotting](https://matplotlib.org/stable/plot_types/3D/index.html)
- [Matplotlib 2D Plotting](https://matplotlib.org/stable/plot_types/basic/index.html)
- [PySimpleGUI Embedded UI](https://www.pysimplegui.org/en/latest/#user-interfaces-for-humans-transforms-tkinter-qt-remi-wxpython-into-portable-people-friendly-pythonic-interfaces)
- [Serial Port Communication using PySerial](https://pyserial.readthedocs.io/en/latest/index.html)
- [Asynchronous Routines in Python - Low Level](https://docs.python.org/3/library/asyncio.html)

### Pandas Help Links

- [Pandas Tutorial on GeeksforGeeks](https://www.geeksforgeeks.org/pandas-tutorial/)
- [Reading CSV files with Pandas](https://www.geeksforgeeks.org/python-read-csv-using-pandas-read_csv/)
- [Reading Excel files with Pandas](https://www.geeksforgeeks.org/loading-excel-spreadsheet-as-pandas-dataframe/?ref=lbp)
- [Plotting a Pandas Dataframe with Matplotlib](https://www.geeksforgeeks.org/how-to-plot-a-pandas-dataframe-with-matplotlib/)