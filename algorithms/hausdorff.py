import numpy as np
import hausdorff

# two random 2D arrays (second dimension must match)
np.random.seed(0)
X = np.random.random((1000,100))
Y = np.random.random((5000,100))

print("Hausdorff distance test: {0}".format( hausdorff.hausdorff(X, Y, distance="euclidean") ))