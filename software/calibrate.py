from driver import Otamatone, Otamatone_State
import sys
o = Otamatone(sys.argv[1])
number_of_pass = 3
cal_res = [[0 for _ in range(8)] for __ in range(number_of_pass)]
for p in range(number_of_pass):
    print("\npass", p + 1)

    for i in range(8):
        print("please press note", i + 1)
        state, value = o.read()
        while state != Otamatone_State.PRESS:
            state, value = o.read()
        cal_res[p][i] = value
    
print(cal_res)