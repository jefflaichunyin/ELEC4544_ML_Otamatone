import  csv
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

''''''
with open('recorder_fingering_test.csv','r') as csv_file:
    lines1 = csv_file.readlines()

lines1[0] = lines1[0].replace("\n","")
data1 = lines1[0].split(',')
print(data1)
dat1=np.array(data1)


with open('recorder_fingering.csv','r') as csv_file:
    lines = csv_file.readlines()

lines[0] = lines[0].replace("\n","")
data = lines[0].split(',')
print(data)
buf = []
for j in range(0,8,1):
    for i in range(0,int(len(data)/8),1):
        buf.append(float(data[8*i+j]))

dat = np.array(buf)
print(dat)

#model = KMeans(n_clusters=8, init='random', random_state=8, max_iter=300000, n_init=1)
model = KMeans(n_clusters=8)
#a = model.fit(np.reshape(dat,(len(dat),1)))
a = model.fit(dat.reshape(-1,1))
centroids = model.cluster_centers_
labels = model.labels_

print(centroids)
print(labels)

colors = ["b.","g.","r.","c.","m.","y.","k.","r."]

#for i in centroids: 
    #plt.plot( [0, len(dat)-1],[i,i], "k" )
for i in range(len(dat)):
    #plt.plot(i,data[i], colors[labels[i]], markersize = 10)
    plt.plot(i,buf[i], colors[labels[i]], markersize = 10)

plt.show()

print(model)
pre=model.predict(dat1.reshape(-1,1))
print(pre)
#y_pred = model.predict(dat.reshape(-1,1))