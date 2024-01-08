from enum import Enum
import numpy as np
import segmentationtools as st
import matplotlib.pyplot as plt

track = st.Segment()
# sig = np.random.randn(200000)
with open('CNN_test_good_long.txt') as f:
    sig = [float(line.rstrip()) for line in f]

# print("track.run", track.run(sig))
# print("sig", sig)
# print("track.status", track.status)
#
# plt.plot(sig)
# plt.ylabel('signal')
# plt.show()

for i in range(1000):
    track.run(sig[i*200:(i+1)*200])
    print("track.status ", track.status)
    print(sig[i*200:(i+1)*200])

# print("track.run", track.run(sig))
# print("sig", sig)
# print("track.status", track.status)

