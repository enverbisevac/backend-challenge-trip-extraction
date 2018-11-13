import json
import os

import matplotlib.pyplot as plt
import numpy as np

import mplleaflet

filename = os.path.join(os.path.dirname(__file__), 'data', 'new_waypoints.json')
with open(filename) as f:
    gj = json.load(f)

xy = np.array([[pos["lng"], pos["lat"]] for pos in gj])

plt.plot(xy[:,0], xy[:,1], 'r.')
plt.plot(xy[:,0], xy[:,1], 'b')

mplleaflet.show()