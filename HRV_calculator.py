import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
from scipy import signal
import math


# Define the path to your .txt file
file_path = "C:\\Users\\mickm\\Zuyd Hogeschool\\AI Stress - Documenten\\General\\Onderzoek\\Onderzoek Biometrie\\Research B\\Data\\A(N01)M.txt"  # Replace with the actual file path

# Initialize variables to keep track of the highest peaks
highest_peak_values = []
highest_peak_indices = []

# Initialize variables to store the data rows
data = []
RMSSD = []


# Open and read the .txt file
with open(file_path, 'r') as file:
    data_started = False  # Flag to indicate when the data begins
    for line in file:
        # Check if the line contains the data
        if data_started:
            # Split each line into values (assuming space-separated)
            values = line.strip().split()
            # Append the values as integers or floats to your data list
            data.append([int(val) for val in values])
        # Check if the line contains the end of the header
        elif line.strip() == "# EndOfHeader":
            data_started = True  # Set the flag to True to indicate the start of data

# Convert the data into a NumPy array for further processing
data = np.array(data)

# Define the data column containing the heartbeat values
heartbeat_data = data[:, 2]

# Find peaks in the original heartbeat data (unfiltered)
# You may need to adjust the threshold as needed for the unfiltered data
heightthreshold = 150  # Adjust this threshold as needed
widthtreshold = 200


#Butterworth filter
sos = signal.butter(2, 3, 'highpass',fs = 1000, output = 'sos')
filtered = signal.sosfilt(sos, heartbeat_data)

# Create an array for the x-axis (time)
time = np.arange(len(heartbeat_data))

peaks, _ = signal.find_peaks(filtered, height=heightthreshold, distance= widthtreshold)

# Plot the original data
HRPlot = plt.figure(figsize=(12, 6))
plt.plot(time, filtered, label='Filtered Data')

# Plot the detected highest peaks on the original data
plt.plot(peaks, filtered[peaks], 'ro', label='Highest Peaks')
plt.xlabel('Time (Row Index)')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Filtered Heartbeat Data with Detected Highest Peaks')
plt.grid(True)
plt.xlim(0,4000)
# Show the plot
HRPlot.show()


interval = 29 #aantal meetpunten per HRV waarde

nulpunt = 0
nulpunt2 = interval

#Calculate HRV with RMSSD
HRV = []
HRVcount = 0
q = 0

for i in range(int(len(peaks)/interval)):
    for j in range(nulpunt, nulpunt2):
        RMSSD.append(math.pow(heartbeat_data[peaks[nulpunt+q+1]] - heartbeat_data[peaks[nulpunt+q]], 2)) #heartbeat_data vervangen door pieken
        q = q+1
    for g in range(interval):
        HRVcount += RMSSD[g]
    HRV.append(HRVcount/(interval-1))
    HRVcount = 0
    q = 0
    RMSSD = []
    nulpunt = nulpunt + interval
    nulpunt2 = nulpunt2 + interval




plt.figure(figsize=(12, 6))
plt.plot(HRV, label='HRV')
plt.xlabel('Time (Row Index)')
plt.ylabel('Amplitude')
plt.title('HRV data')
plt.grid(True)
plt.xlim(0,200)
plt.show()

#test
#Calculate HRV with SDNN