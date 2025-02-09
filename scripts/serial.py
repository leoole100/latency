#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script to measure time and and error rate of a serial connection
"""

# %%
import serial
import serial.tools.list_ports
import numpy as np
import time
from tqdm import tqdm
from scipy.stats import norm

# %%
# try to connect to a default port
ser = serial.Serial('/dev/ttyUSB0', 115200)

# %%
N = int(1e5)
data = np.zeros((N, 2))
start = time.time()

def ping():
	ser.write(b'1')
	response = ser.read(1)
	return response

response = ping()

for i in tqdm(range(N)):
	start = time.time()
	response = ping()
	end = time.time()
	data[i, 0] = end - start
	data[i, 1] = (response != b'1')

# %%
import matplotlib.pyplot as plt
density, bins = np.histogram(data[:, 0], bins=1000)

# calculate the error rate
error_rate = np.mean(data[:, 1])
if error_rate == 0:
	error_rate_string = f"<1e{int(np.log10(1/N))}"
else:
	error_rate_string = f'{error_rate:.2g}'

plt.figure()
plt.step(bins*1e6, np.append(density, 0)/1e6)

plt.text(0.95, 0.95, 
f"""N = 1e{int(np.log10(N))}
Mean: {np.mean(data[:, 0])*1e6:.2f} us
σ: {np.std(data[:, 0])*1e6:.2f} us
Max: {np.max(data[:, 0])*1e6:.2f} us
Error rate: {error_rate_string}
""", 
	horizontalalignment='right', 
	verticalalignment='top', 
	transform=plt.gca().transAxes)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('time in μs')
plt.ylabel('rate in 1/μs')
plt.savefig('../figures/pyserial.png')
plt.show()
# %%
