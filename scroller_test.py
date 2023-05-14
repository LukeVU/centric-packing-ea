import matplotlib.pyplot as plt
import numpy as np
import mplcursors

fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(20, 20))

for i in range(3):
    for j in range(3):
        axs[i, j].plot(np.random.randn(100), label=f"subplot({i+1}, {j+1})")
        axs[i, j].legend()

plt.tight_layout()

mplcursors.cursor(hover=True)

plt.show()
