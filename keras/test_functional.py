from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Activation, Input
import matplotlib.pyplot as plt
import numpy as np


DATASET_DIR = 'mnist_train.csv'
def get_data(image_show=False):
    reading = True
    X = []
    Y = []
    print(f'Reading {DATASET_DIR}...')
    with open(DATASET_DIR) as file:
        file.readline()
        while reading:
            try:
                line = file.readline()
                Y.append(int(line[0]))
                X.append([float(number)/255. for number in line[2:].strip().split(',')])
            except:
                reading = False
    print('Finished')
        
    X_copy = []
    Y_copy = []
            
    print(len(Y))
    print(len(X))
    randomize = np.arange(0, len(Y), 1)
    np.random.shuffle(randomize)
    print(randomize)

    for i in range(len(Y)):
        X_copy.append(X[randomize[i]])
        Y_copy.append(Y[randomize[i]])
    
    X = X_copy
    Y = Y_copy

    if image_show:
        plt.title(Y[0])
        x = np.zeros((28, 28))
        for i in range(28):
            for j in range(28):
                x[i,j] = X[0][i*28 + j]
        plt.imshow(x)
        plt.show()
    return np.array(X), np.array(Y)

def y2indicator(Y):
    K = len(set(Y))
    N = len(Y)
    Y_ind = np.zeros((N, K))
    for i in range(N):
        Y_ind[i, Y[i]] = 1
    return Y_ind
    

def main():
    X, Y = get_data(True)

    N, D = X.shape
    K = len(set(Y))
    
    Y = y2indicator(Y)

    i = Input(shape=(D,))
    x = Dense(units=500, activation='relu')(i)
    x = Dense(units=300, activation='relu')(x)
    x = Dense(units=K, activation='softmax')(x)
    model = Model(inputs=i, outputs=x)

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    
    r = model.fit(X, Y, validation_split=0.2, epochs=15, batch_size=32)
    print(f'Returned: {r}')

    plt.plot(r.history['loss'], label='loss')
    plt.plot(r.history['val_loss'], label='val_loss')
    plt.legend()
    plt.show()
if __name__ == '__main__':
    main()