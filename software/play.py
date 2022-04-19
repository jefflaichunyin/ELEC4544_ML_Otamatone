from driver import Otamatone, Otamatone_State
from midi import Midi
import sys
o = Otamatone(sys.argv[1])
m= Midi(int(sys.argv[2]))
prev_pos = 0

def clamp(a, minimum, maximum):
    return max(minimum, min(a,maximum))

while True:
    state, value = o.read()
    if state == Otamatone_State.PRESS:
        print("pressed", value)
        m.play(value / 10)
    elif state == Otamatone_State.RELEASE:
        print("release")
        m.stop()
    elif state == Otamatone_State.HOLD:
        press_pos, cur_pos = value
        bend_val = clamp((cur_pos-press_pos) * 4 , -8192, 8191)
        m.bend(bend_val)

    