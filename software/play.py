from driver import Otamatone, Otamatone_State
from midi import Midi
from predict import Note_Predictor
import sys
import time

TIMEOUT = 3
o = Otamatone(sys.argv[1])
m= Midi(int(sys.argv[2]))
p = Note_Predictor(sys.argv[3])

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def clamp(a, minimum, maximum):
    return max(minimum, min(a,maximum))

print("Ready")
prev_press = time.time()
while True:
    state, value = o.read()
    if state == Otamatone_State.PRESS:
        print("pressed", value)
        m.play_note(p.predict_note(value))
    elif state == Otamatone_State.RELEASE:
        prev_press = time.time()
        print("release")
        m.stop()
    elif state == Otamatone_State.HOLD:
        prev_press = time.time()
        press_pos, cur_pos = value
        # print('hold', press_pos)
        # note = p.predict_note(cur_pos)
        # if m.playing != note:
        #     m.play_note(note)

        # bend_val = clamp((cur_pos-press_pos) * 2 , -8192, 8191)
        # m.bend(bend_val)
    if time.time() - prev_press > TIMEOUT:
        print('TIMEOUT')
        prev_press = time.time()
        p.reset_state()

    