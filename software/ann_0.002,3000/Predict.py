'''
0:d,1:r,2:m,3=f,4=s,5=l,6=t,7=d'

'''

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
import matplotlib.pyplot as plt
from keras.models import load_model

#Load data
test_data=pd.read_csv("recorder_fingering_test-Copy2.csv",header=None)


#define variables
test_samples=[]
test_labels=[]

test_data=np.array(test_data)

for i in range(48):
    test_samples.append(test_data[0][i])
for i in range(48):
    test_labels.append(test_data[1][i])

test_labels=np.array(test_labels)
test_samples=np.array(test_samples)
test_labels,test_samples=shuffle(test_labels,test_samples)

#Prediction
model = load_model('ann4.h5')
predict=model.predict(test_samples,verbose=1)
k=np.argmax(predict, axis=1)
print("Predict:")
print(k)

#Confidence of prediction
confidence=[]
for i in range(48):
    confidence.append(max(predict[i]))
print("Confidence:")
print(confidence)

#Change to midi number
midi_no=[]
for i in range(len(k)):
    if(k[i]==0):
        midi_no.append('60')
    elif(k[i]==1):
        midi_no.append('62')
    elif(k[i]==2):
        midi_no.append('64')
    elif(k[i]==3):
        midi_no.append('65')
    elif(k[i]==4):
        midi_no.append('67')
    elif(k[i]==5):
        midi_no.append('69')
    elif(k[i]==6):
        midi_no.append('71')
    elif(k[i]==7):
        midi_no.append('72')
print("Midi number:")
print(midi_no)

#Evaluate
model.evaluate(test_samples,test_labels)