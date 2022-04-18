import pygame.midi as midi

class Midi:

    def __init__(self) -> None:
        midi.init()
        self.out = midi.Output(2)
        self.out.set_instrument(31)
        self.playing = 0

    def play(self, freq):
        self.stop()
        self.playing = midi.frequency_to_midi(freq)
        print("play", self.playing)
        self.out.note_on(self.playing, 127)

    def stop(self):
        if self.playing != 0:
            print("stop", self.playing)
            self.out.note_off(self.playing, 127)

    def bend(self, v):
        self.out.pitch_bend(v)