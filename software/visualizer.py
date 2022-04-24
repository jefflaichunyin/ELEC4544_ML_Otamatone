import matplotlib.pyplot as plt

plt.ion()
plt.show()

fig, ax = plt.subplots(2, figsize=(15, 8))
ax[0].set_title('Position Input')
ax[1].set_title('Note prediction')

input("Press [enter] to continue.")