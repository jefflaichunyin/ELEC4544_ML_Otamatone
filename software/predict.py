import mido
import sys
o = Otamatone(sys.argv[1])
m= Midi(int(sys.argv[2]))
f = mido.MidiFile(sys.argv[3])
notes = list(map(lambda x: x.note, filter(lambda x : x.velocity == 80, m.tracks[0][11:-1])))