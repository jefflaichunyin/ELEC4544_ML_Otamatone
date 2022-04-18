import pygame.midi as midi
import time
midi.init()
out = midi.Output(2)
out.set_instrument(31)
out.note_on(16,127)
time.sleep(2)
out.note_off(64,127)
out.close()
