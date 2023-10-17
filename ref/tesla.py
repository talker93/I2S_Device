from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

# Question 1:
# Fill array x with L seconds of sine function, with frequency f0, sample rate fs.

fs = 48000 # sample rate
L = 2      # seconds
f0 = 1000  # signal frequency Hz
x = np.zeros(L*fs)
for i in range(L*fs):
    x[i] = np.sin(2*np.pi*f0/fs*i)

print(x.shape)

# Question 2:
# Design a butterworth lowpass filter and apply to x saving output in y. Use scipy.signal.butter
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html

Norder = 2
Wn = 0.5

b, a = signal.butter(Norder, Wn*fs/2, 'low', analog=True)
y = signal.filtfilt(b, a, x)
print(y.shape)

w, h = signal.freqs(b, a)
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(100, color='green') # cutoff frequency
plt.show()

import csv
# Question 3
# Read in csv file '/home/coderpad/data/inverter_raw_output.csv' and print out the header and the first 10 rows of data in csv format, i.e.
# dt, signal_value, signal_name
# 9/5/2019 0:30, 1.074725061, inv_i_out
# 9/5/2019 0:35, 1.062872009, inv_i_out
# ...
print('')
print('Question 3 output:')

#with open('/home/coderpad/data/inverter_raw_output.csv') as csvfile:
# ...

# Question 4
# Read in csv file and print header and then only the rows (in csv format) where signal_value > THRESHOLD and the signal is inv_i_out
THRESHOLD = 7.

#with open('/home/coderpad/data/inverter_raw_output.csv') as csvfile:
# ...

# Question 5
# The file contains corresponding entires for inv_i_out and inv_v_out for each timestamp dt. Read in csv file and print a header row, (in csv format) and then rows with dt, the inv_i_out value and inv_v_out value for all cases where inv_i_out > THRESHOLD
# i.e.
# dt, inv_i_out, inv_v_out
# 9/5/2019 0:30, 1.074725061, 235.32958727
# 9/5/2019 0:35, 1.062872009, 234.5672375
# ...

print('')
print('Question 5 output:')

#with open('/home/coderpad/data/inverter_raw_output.csv') as csvfile:
# ...