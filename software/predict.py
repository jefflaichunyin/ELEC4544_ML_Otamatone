from sklearn import svm
import numpy as np
class Note_Predictor:

    def __init__(self, training_data) -> None:
        samples, labels = np.loadtxt('recorder_fingering_test.csv', delimiter=',', dtype=int)
        clf = svm.SVC()
        clf.fit(samples.reshape(-1,1), labels)
        self.clf = clf

    def predict_note(self, position):
        return self.clf.predict([[position]])[0]