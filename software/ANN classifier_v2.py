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
from sklearn.model_selection import train_test_split
from keras.models import load_model

#Load data
train_data=pd.read_csv("recorder_fingering.csv",header=None)

#Define variables
train_samples=[]
train_labels=[]

for i in range(480):
    train_samples.append(train_data[0][i])
for i in range(480):
    train_labels.append(train_data[1][i])

train_labels=np.array(train_labels)
train_samples=np.array(train_samples)

#Split into train and test data
X_train, X_test, y_train, y_test = train_test_split(train_samples,train_labels, test_size=0.2, random_state=20)

#Shuffle data
y_train=np.array(y_train)
X_train=np.array(X_train)
y_train,X_train=shuffle(y_train,X_train)
y_test=np.array(y_test)
X_test=np.array(X_test)
y_test,X_test=shuffle(y_test,X_test)

#Data preprocessing
scaler=MinMaxScaler(feature_range=(0,1))
scaled_X_train=scaler.fit_transform(X_train.reshape(-1,1))
scaled_X_test=scaler.fit_transform(X_test.reshape(-1,1))

#Model layers
model=Sequential([Dense(units=64,input_shape=(1,),activation='relu'),
                 Dense(units=32,activation='relu'),
                 Dense (units=8,activation='softmax')])
model.summary()

#Training
model.compile(optimizer=Adam(learning_rate=0.0001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
history=model.fit(x=scaled_X_train,y=y_train,epochs=3000,validation_data=(scaled_X_test, y_test),verbose=1)

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
model.save("randomdata_ann.h5")

#Load .h5 model and predict
model = load_model('randomdata_ann.h5')
model.predict(X_test)