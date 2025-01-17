"""Graphics functions"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def binary_animate(data: np.ndarray) -> None:
    """Animate 2D binary video
    
    Parameter
    ---------
    data : np.ndarray
        frames x rows x columns
    """
    
    fig, ax = plt.subplots()
    im = ax.imshow(data[0], cmap='binary')
    # ax.axis('off')

    def update(frame_idx) -> np.ndarray:
        im.set_data(data[frame_idx])
    
    ani = FuncAnimation(fig, update, frames=data.shape[0])
    plt.close()
    return HTML(ani.to_jshtml())