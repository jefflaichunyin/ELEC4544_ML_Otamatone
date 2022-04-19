import pygame.midi as midi

class Midi:

    def __init__(self, dev_id) -> None:
        midi.init()
        self.out = midi.Output(dev_id)
        self.out.set_instrument(57)
        self.playing = 0

    def play(self, freq):
        self.stop()
        self.playing = midi.frequency_to_midi(freq)
        print("play", self.playing)
        self.out.note_on(self.playing, 127)

    def play_note(self, note):
        self.stop()
        self.playing = note
        print("play", self.playing)
        self.out.note_on(self.playing, 127)
        
    def stop(self):
        if self.playing != 0:
            # print("stop", self.playing)
            self.out.note_off(self.playing, 127)

    def bend(self, v):
        self.out.pitch_bend(v)