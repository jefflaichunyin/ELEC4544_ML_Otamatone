from sklearn import svm
from keras.models import load_model
import numpy as np
from sklearn import preprocessing, tree
import mido

def pad_seq(seq, win_size_max):
    return seq + [0]*(win_size_max-len(seq))

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
    def __init__(self, midi_file) -> None:
        self.model = load_model('trained_model.h5')
        self.win_size_max = 3
        self.seq = [0 for x in range(self.win_size_max)]
        f = mido.MidiFile('1.mid')
        self.midi_notes = list(map(lambda x: x.note, filter(lambda x : x.velocity == 80, f.tracks[0][11:-1])))
        self.init_decision_tree()

    def push_prediction(self, note):
        # self.seq.pop(-1)
        # self.seq = [note] + self.seq
        if 0 in self.seq:
            # fill it first
            self.seq[self.seq.index(0)] = note
        else:
            self.seq.pop(0)
            self.seq = self.seq + [note] 

    def init_decision_tree(self):
        self.dt = tree.DecisionTreeClassifier()
        song_len = len(self.midi_notes)
        transitions = []
        nexts = []
        for window_size in range(1, self.win_size_max+1):
            for base in range(song_len-window_size):
                window = self.midi_notes[base:base+window_size] + [0] * (self.win_size_max-window_size)
                next = self.midi_notes[base+window_size]
                transitions += [window]
                nexts += [next]

        self.dt.fit(transitions, nexts)

    def predict_note(self, position):
        notes = [60,62,64,65,67,69,71,72]
        enc = preprocessing.LabelEncoder()
        enc.fit(notes)
        predictions = self.model.predict([position])
        predicted = np.argmax(predictions)
        note = enc.inverse_transform([predicted])[0]
        if sum(self.seq) == 0:
            # no history yet, rely on NN solely
            predictions = self.model.predict([position])
            print('no history predict with NN', predictions)
            predicted = np.argmax(predictions)
            note = notes[predicted]
        else:
            # use decision tree to help
            dt_prob = [0 for _ in range(len(notes))]
            dt_pred = self.dt.predict_proba([self.seq])[0]
            for c in self.dt.classes_:
                idx = np.where(self.dt.classes_ == c)
                # idx = t.classes_.where(c)
                prob = dt_pred[idx][0]
                idx = notes.index(c)
                dt_prob[idx] = prob

            dt_prob = np.array(dt_prob)
            nn_prob = self.model.predict([position])[0]
            cm_prob = dt_prob * nn_prob
            print(self.seq)
            print('DT prediction', np.array_str(dt_prob, precision=2))
            print('NN prediction', np.array_str(nn_prob, precision=2))
            print('Combined prediction', np.array_str(cm_prob, precision=2))
            note = notes[np.argmax(cm_prob)]

        self.push_prediction(note)
        return note
