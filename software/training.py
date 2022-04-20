import numpy as np
position, label = np.loadtxt('calibration_data.csv', delimiter=',', dtype=int)
plt.scatter(position, label)
plt.show()
