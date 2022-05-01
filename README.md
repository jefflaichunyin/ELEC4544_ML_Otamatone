# COMP4544_Otamatone
Predict Otamatone output pitch from press position using machine learning algorithm.

## Dependencies
```pip install pygame numpy matplotlib sklearn tensorflow pyserial mido```

## Collect Training data
```./collect.py [PORT] [MIDI CHANNEL e.g. 0]```

## Train the model
- Run the classifier.ipynb jupyter notebook, it takes ```training_data.csv``` as input and outputs ```trained_model.h5```

## Play
- Level 0

  Map press position to output notes linearly
  
  ```./play.py [PORT] [MIDI CHANNEL e.g. 0]```
- Level 1

  Map press position to output notes using Artificial Neural Network
  
  ```./play.py [PORT] [MIDI CHANNEL e.g. 0] trained_model.h5```
- Level 2

  Map press position to output notes using Artificial Neural Network and Decision Tree
  
  ```./play.py [PORT] [MIDI CHANNEL e.g. 0] trained_model.h5 mary_had_a_little_lamb.mid```
