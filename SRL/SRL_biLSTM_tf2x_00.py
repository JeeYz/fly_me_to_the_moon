# -*- coding: utf-8 -*-

#%% declaration variables
file0 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_raw_train_data_index_0.txt"
file1 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_raw_test_data_index_0.txt"


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import sys
import numpy as np


print('Python version : ', sys.version)
print('TensorFlow version : ', tf.__version__)
print('Keras version: ', keras.__version__)

VEC_SIZE = 64
WORDS_SIZE = 18806
input_len = 53

#%% functions
def load_train_data():
    xtrain, ytrain = list(), list()
    xtest, ytest = list(), list()

    with open(file0, 'r', encoding='utf-8') as f0,\
    open(file1, 'r', encoding='utf-8') as f1:
        while True:
            line = f0.readline()
            if not line:break
            line = line.split()
            xtrain.append(np.asarray(line[:-1], dtype='float64'))
            ytrain.append(np.asarray(line[-1], dtype='float64'))
            
        while True:
            line = f1.readline()
            if not line:break
            line = line.split()
            xtest.append(np.asarray(line[:-1], dtype='float64'))
            ytest.append(np.asarray(line[-1], dtype='float64'))
        xtrain = np.asarray(xtrain)
        ytrain = np.asarray(ytrain)
        xtest = np.asarray(xtest)
        ytest = np.asarray(ytest)
    return xtrain, ytrain, xtest, ytest



#%% load train data
xtrain, ytrain, xtest, ytest = load_train_data()


#%% embedding layer
embedding_layer = layers.Embedding(WORDS_SIZE, VEC_SIZE, \
                                    embeddings_initializer='uniform')

    
#%% input layer   
w_input =  tf.keras.Input(shape=(53), name='w_input')


#%% embedding
x = embedding_layer(w_input)


#%% setting LSTM layer
forward = layers.LSTM(128)
backward = layers.LSTM(128, go_backwards=True)


#%% LSTM layer
x = layers.Bidirectional(forward, backward_layer=backward)(x)
x = layers.Dense(512, activation='relu')(x)
x = layers.Dropout(0.2)(x)


#%% output layer
answer = layers.Dense(16, activation='softmax')(x)


#%% model declaration
model = tf.keras.Model(inputs=w_input, outputs=answer)
model.summary()


#%%
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


history = model.fit(xtrain, ytrain, batch_size=32, epochs=10)

results = model.evaluate(xtest, ytest, verbose=2)





