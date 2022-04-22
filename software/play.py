from driver import Otamatone, Otamatone_State
from midi import Midi
from predict import Note_Predictor
import sys

o = Otamatone(sys.argv[1])
m= Midi(int(sys.argv[2]))
p = Note_Predictor(sys.argv[3])

prev_pos = 0

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def clamp(a, minimum, maximum):
    return max(minimum, min(a,maximum))

while True:
    state, value = o.read()
    if state == Otamatone_State.PRESS:
        print("pressed", value)
        m.play_note(p.predict_note(value))
    elif state == Otamatone_State.RELEASE:
        print("release")
        m.stop()
    elif state == Otamatone_State.HOLD:
        pass
        # press_pos, cur_pos = value
        # bend_val = clamp((cur_pos-press_pos) * 4 , -8192, 8191)
        # m.bend(bend_val)

    