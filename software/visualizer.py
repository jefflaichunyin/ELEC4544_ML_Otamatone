import matplotlib.pyplot as plt

class Visualizer:
    
    def __init__(self) -> None:
        self.running = True

    def start(self):
        self.notes = [60,62,64,65,67,69,71,72]
        fig, ax = plt.subplots(2, 2, figsize=(15, 10))
        fig.canvas.mpl_connect('close_event', self.on_close)
        pos, res, nn, dt = (ax[0,0], ax[0,1], ax[1,0], ax[1,1])
        pos.set_yticks(self.notes)
        pos.set_ylim(55, 75)
        pos.set_title('Position Input')
        res.set_title('Prediction result')
        res.set_ylim(0,1.1)
        nn.set_title('NN prediction')
        nn.set_ylim(0,1.1)
        dt.set_title('Decision Tree prediction')
        dt.set_ylim(0,1.1)

        res.set(xlabel='Note', ylabel='Probability')
        nn.set(xlabel='Note', ylabel='Probability')
        dt.set(xlabel='Note', ylabel='Probability')

        self.prev_plt = [None, None, None, None]
        self.ax = ax
        plt.ion()
        plt.draw()
        plt.pause(0.0001)
        plt.show()

    def on_close(self, event):
        self.running = False

    def draw(self):
        plt.draw()
        plt.pause(0.01)

    def plot(self, seq, res_prob, nn_prob, dt_prob):
        ax = self.ax
        notes = self.notes
        pos, res, nn, dt = (ax[0,0], ax[0,1], ax[1,0], ax[1,1])
        for p in self.prev_plt:
            if p:
                p.remove()
        pos.set_xticks (range(len(seq)))
        self.prev_plt = pos.bar(range(len(seq)), seq, color='b'), res.scatter(notes, res_prob, color='b'), nn.scatter(notes, nn_prob, color='b'), dt.scatter(notes, dt_prob, color='b')
        # plt.draw()
        plt.pause(0.0001)
