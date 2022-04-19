from driver import Otamatone, Otamatone_State
import sys
import numpy as np
import matplotlib.pyplot as plt

o = Otamatone(sys.argv[1])
number_of_pass = 3
tone_cnt = 8

cal_res = [[0 for _ in range(8)] for __ in range(number_of_pass)]
for p in range(number_of_pass):
    print("\npass", p + 1)

    for i in range(tone_cnt):
        print("please press note", i + 1)
        state, value = o.read()
        while state != Otamatone_State.PRESS:
            state, value = o.read()
        cal_res[p][i] = value
cal_res = np.array(cal_res).T
y =  [([x]*number_of_pass) for x in range(tone_cnt)]
plt.scatter(cal_res, y)
plt.show()
