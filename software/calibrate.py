from driver import Otamatone, Otamatone_State
from midi import Midi

import sys
import numpy as np
import matplotlib.pyplot as plt

o = Otamatone(sys.argv[1])
m= Midi(int(sys.argv[2]))

target_note = [60,62,64,65,67,69,71,72]
number_of_pass = 3
tone_cnt = 8

position = []
label = []

for p in range(number_of_pass):
    print("\npass", p + 1)

    for i in range(tone_cnt):
        print("please press note", i + 1)
        m.play_note(target_note[i])
        state, value = o.read()
        while state != Otamatone_State.PRESS:
            state, value = o.read()
        
        position += [value]
        label += [target_note[i]]

        m.stop()

position = np.array(position)
label = np.array(label)
np.savetxt('calibration_data.csv', (position, label), fmt='%i', delimiter=',')

plt.scatter(position, label)
plt.show()
