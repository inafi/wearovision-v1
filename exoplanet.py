import tensorflow as tf
import csv
import numpy as np
from keras.layers import Dense, Dropout
from keras.utils.vis_utils import plot_model

def getdata(path):
    arr = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in reader: # each row is a list
            arr.append(row)
    x = []
    y = []
    for i in range(1, len(arr)):
        y.append(int(arr[i][0] - 1))
        r = arr[i]
        del r[0]
        x.append(r)
    return x, y

x_train, y_train = getdata("/Users/nafi/Develop/ML/Exoplanet/Data/exoTrain.csv")

y_train = np.array(y_train)

x_train = tf.keras.utils.normalize(x_train, axis = 1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(10, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(2, activation = tf.nn.softmax))

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=['accuracy'])

import matplotlib.pyplot as plt

history = model.fit(x_train, y_train, validation_split=0.25, epochs=6, batch_size=16, verbose=1)

# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()