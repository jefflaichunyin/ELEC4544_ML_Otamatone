from sklearn import svm
from keras.models import load_model
import numpy as np
from sklearn import tree
import mido


def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

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
    def __init__(self, nn_model = None, midi_file = None) -> None:
        self.win_size_max = 3
        self.pos_hist = [0 for x in range(self.win_size_max)]
        self.seq = [0 for x in range(self.win_size_max)]
        self.nn = None
        self.dt = None

        if nn_model:
            self.init_nn(nn_model)
        if midi_file:
            self.init_decision_tree(midi_file)

    def init_nn(self, nn_model):
        self.nn = load_model(nn_model)

    def init_decision_tree(self, midi_file):
        f = mido.MidiFile(midi_file)
        self.midi_notes = list(map(lambda x: x.note, filter(lambda x : x.velocity == 80, f.tracks[0][11:-1])))
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

    def reset_state(self):
        self.seq = [0 for x in range(self.win_size_max)]
        self.pos_hist = [0 for x in range(self.win_size_max)]
        
    def push_prediction(self, note):
        # self.seq.pop(-1)
        # self.seq = [note] + self.seq
        if 0 in self.seq:
            # fill it first
            self.seq[self.seq.index(0)] = note
        else:
            self.seq.pop(0)
            self.seq = self.seq + [note] 

    def predict_note(self, position):
        notes = [60,62,64,65,67,69,71,72]
        res_prob = [0 for _ in range(len(notes))]
        nn_prob = [0 for _ in range(len(notes))]
        dt_prob = [0 for _ in range(len(notes))]
        self.pos_hist.pop(0)
        self.pos_hist = self.pos_hist + [position] 
        print(self.pos_hist)
        if self.nn is None:
            predicted = _map(position, 1000, 6000, 0, 7)
            ln_prob = [0 for _ in range(8)]
            ln_prob[predicted] = 1.0
            res_prob = np.array(ln_prob)
        elif self.dt is None or sum(self.seq) == 0:
            # no history yet, rely on NN solely
            nn_prob = self.nn.predict([position])[0]
            res_prob = nn_prob
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
            nn_prob = self.nn.predict([position])[0]
            res_prob = dt_prob * nn_prob

        return (self.pos_hist, res_prob, nn_prob, dt_prob)
