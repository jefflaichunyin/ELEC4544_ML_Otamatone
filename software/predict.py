from sklearn import svm
from keras.models import load_model
import numpy as np
from sklearn import preprocessing

class Note_Predictor:

    # predict with SVM
    # def __init__(self, training_data) -> None:
    #     samples, labels = np.loadtxt('recorder_fingering_test.csv', delimiter=',', dtype=int)
    #     clf = svm.SVC()
    #     clf.fit(samples.reshape(-1,1), labels)
    #     self.clf = clf

    # def predict_note(self, position):
    #     return self.clf.predict([[position]])[0]

    # predict with NN
    def __init__(self, _) -> None:
        self.model = load_model('trained_model.h5')

    def predict_note(self, position):
        notes = [60,62,64,65,67,69,71,72]
        enc = preprocessing.LabelEncoder()
        enc.fit(notes)
        predictions = self.model.predict([position])
        predicted = np.argmax(predictions)
        note = enc.inverse_transform([predicted])[0]
        return note
