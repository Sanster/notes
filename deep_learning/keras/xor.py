import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense

# the four different states of the XOR gate
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], "float32")

# the four expected results in the same order
y = np.array([[0], [1], [1], [0]], "float32")

model = Sequential()
model.add(Dense(16, input_dim=2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['binary_accuracy'])

model.fit(X, y, nb_epoch=500, verbose=2)

print(model.predict(X).round())
