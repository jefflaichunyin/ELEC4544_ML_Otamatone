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
train_data=pd.read_csv("recorder_fingering-Copy2.csv",header=None)
test_data=pd.read_csv("recorder_fingering_test-Copy2.csv",header=None)


#define variables
train_samples=[]
train_labels=[]
test_samples=[]
test_labels=[]

train_data=np.array(train_data)
test_data=np.array(test_data)

for i in range(432):
    train_samples.append(train_data[0][i])
for i in range(432):
    train_labels.append(train_data[1][i])
for i in range(48):
    test_samples.append(test_data[0][i])
for i in range(48):
    test_labels.append(test_data[1][i])

train_labels=np.array(train_labels)
train_samples=np.array(train_samples)
train_labels,train_samples=shuffle(train_labels,train_samples)
test_labels=np.array(test_labels)
test_samples=np.array(test_samples)
test_labels,test_samples=shuffle(test_labels,test_samples)

#Data preprocessing
scaler=MinMaxScaler(feature_range=(0,1))
scaled_train_samples=scaler.fit_transform(train_samples.reshape(-1,1))
scaled_test_samples=scaler.fit_transform(test_samples.reshape(-1,1))

#Model
model=Sequential([Dense(units=64,input_shape=(1,),activation='relu'),
                 Dense(units=32,activation='relu'),
                 Dense (units=8,activation='softmax')])
model.summary()

#Training
model.compile(optimizer=Adam(learning_rate=0.001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
history=model.fit(x=train_samples,y=train_labels,epochs=1000,validation_data=(test_samples, test_labels),verbose=1)

#Plot graph
plt.plot(history.history['accuracy'])
plt.title('Training accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')

plt.plot(history.history['loss'])
plt.title('Training loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')

plt.plot(history.history['val_accuracy'])
plt.title('Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')

plt.plot(history.history['val_loss'])
plt.title('Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')

#Save model
model.save('ann.h5')

