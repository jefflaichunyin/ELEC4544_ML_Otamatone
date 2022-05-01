# COMP4544_Otamatone

## Dependencies
```pip install pygame numpy matplotlib sklearn tensorflow pyserial mido```

## Usage
- Level 0
Map press position to output notes linearly
```./play.py [PORT] [MIDI CHANNEL e.g. 0]```
- Level 1
Map press position to output notes using Artificial Neural Network
```./play.py [PORT] [MIDI CHANNEL e.g. 0] trained_model.h5```
- Level 2
```./play.py [PORT] [MIDI CHANNEL e.g. 0] trained_model.h5 mary_had_a_little_lamb.mid```
