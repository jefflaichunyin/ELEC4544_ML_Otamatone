from driver import Otamatone, Otamatone_State
from midi import Midi

import sys
import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

'''
Collect pressing postion of notes and output to an csv file
'''

o = Otamatone(sys.argv[1])
m= Midi(int(sys.argv[2]))

collected_valid_data = False
while not collected_valid_data:
    # Part 1. collect position for notes in an octave
    target_note = [60,62,64,65,67,69,71,72]
    number_of_pass = 30
    tone_cnt = 8

    position = []
    label = []

    for p in range(number_of_pass):
        print("\npass", p + 1)

        for i in range(tone_cnt):
            print("please press note", i + 1)
            m.play_note(target_note[i])
            state, value = o.read()
            while state != Otamatone_State.PRESS:
                state, value = o.read()
            
            position += [value]
            label += [target_note[i]]

            m.stop()

    position = np.array(position)
    label = np.array(label)

    plt.scatter(label, position)
    plt.title('Collected position vs notes')
    plt.xlabel('Note')
    plt.ylabel('Positon')
    plt.show()

    # Part 2. Evaluate the quality of training data
    km = KMeans(n_clusters=8)
    km.fit(position.reshape(-1,1))
    centroids = sorted(km.cluster_centers_)
    labels = km.labels_

    colors = ["b","g","r","c","m","y","k","orange"]

    prediction = km.predict(position.reshape(-1,1))
    mispredicted = []
    for i in range(len(position)):
        predicted = list(km.labels_).index(km.predict([[position[i]]])[0])
        if predicted != i%8:
            plt.plot(i%8, position[i], colors[predicted], marker='s', markersize = 10)
            mispredicted += [i]
        else:
            plt.plot(i%8, position[i], colors[predicted], marker='.', markersize = 10)

    for i in range(len(centroids)):
        plt.plot(i,centroids[i], colors[i], marker='x', markersize = 20)


    plt.title('Clustering result')
    plt.xlabel('Note')
    plt.ylabel('Positon')

    h1 = mlines.Line2D([], [], color='blue', marker='s', linestyle='None',
                            markersize=10, label='mismatch')
    h2 = mlines.Line2D([], [], color='red', marker='.', linestyle='None',
                            markersize=10, label='match')
    h3 = mlines.Line2D([], [], color='purple', marker='x', linestyle='None',
                            markersize=10, label='centroid')
    plt.legend(handles=[h1,h2,h3])
    plt.show()


    # Part 3. Ask user to decide re-collect, remove bad sample or ignore them
    if len(mispredicted):
        print('Detected mismatch between predicted and acutal note')
        choice = int(input('(1) Re-collect, (2) Remove mismatch notes, (3) Ignore mismatch notes: '))
        if choice == 1:
            collected_valid_data = False
        elif choice == 2:
            position = list(position)
            label = list(label)
            for m in mispredicted[::-1]:
                p = position.pop(m)
                l = label.pop(m)
                print(f'removed note {l} position {p} from training data set')
            collected_valid_data = True
        elif choice == 3:
            collected_valid_data = True
        else:
            print('Invalid choice')
    else:
        collected_valid_data = True

print('Outputted training data to training_data.csv')

np.savetxt('training_data.csv', (position, label), fmt='%i', delimiter=',')