from driver import Otamatone, Otamatone_State
from predict import Note_Predictor
from visualizer import Visualizer

from threading import Thread
from midi import Midi
import numpy as np
import sys
import time

TIMEOUT = 3

running = True
notes = [60,62,64,65,67,69,71,72]

res_prob = [0 for _ in range(len(notes))]
nn_prob = [0 for _ in range(len(notes))]
dt_prob = [0 for _ in range(len(notes))]
o = Otamatone(sys.argv[1])
m= Midi(int(sys.argv[2]))


nn_model = None
midi_file = None
if len(sys.argv) > 3:
    nn_model =  sys.argv[3]
if len(sys.argv) > 4:
    midi_file = sys.argv[4]
p = Note_Predictor(nn_model, midi_file)

v = Visualizer()
def plot_thread():
    v.start()
    while v.running:
        v.plot(p.seq, res_prob, nn_prob, dt_prob)

def clamp(a, minimum, maximum):
    return max(minimum, min(a,maximum))

pt = Thread(target=plot_thread)
pt.start()

print("Ready")
prev_press = time.time()
while v.running:
    state, value = o.read()
    if state == Otamatone_State.PRESS:
        print("pressed", value)
        seq, res_prob, nn_prob, dt_prob = p.predict_note(value)
        predicted = predicted = np.argmax(res_prob)
        note = notes[predicted]
        p.push_prediction(note)
        m.play_note(note)
        # v.plot(p.seq, res_prob, nn_prob, dt_prob)
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
        # v.draw()