import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math as m
import keras as k
from sklearn import preprocessing
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, merge, Input, Activation
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.utils import np_utils
from keras.regularizers import l1l2, activity_l2, l2, l1
from keras.optimizers import SGD, Adadelta, Adam
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping

path = '/home/someone/桌面/project3_cnn'
training_data_120u = np.load(str(path)+'/training_data_120u_roll10_best.npy')
test_data_120u = np.load(str(path)+'/test_data_120u_roll10_best.npy')

label_120u = np.load(str(path)+'/label_120u_roll10_best.npy')
label_120u = label_120u[:,2]
label_test_120u = np.load(str(path)+'/label_test_120u_roll10_best.npy')
label_test_120u = label_test_120u[:,2]

'''scaling'''
training_data_120u = np.reshape(training_data_120u,(8760,25))
a= np.zeros((8760, 1))
for i in range(training_data_120u.shape[1]):
    X_scaled = preprocessing.scale(training_data_120u[:,i])
    X_scaled = np.reshape(X_scaled,(8760,1))
    a = np.hstack((a,X_scaled))
training_data_120u = np.delete(a, (0), axis=1)
training_data_120u = np.reshape(training_data_120u,(292,30,25,1))

test_data_120u = np.reshape(test_data_120u,(2160,25))
a= np.zeros((2160, 1))
for i in range(test_data_120u.shape[1]):
    X_scaled = preprocessing.scale(test_data_120u[:,i])
    X_scaled = np.reshape(X_scaled,(2160,1))
    a = np.hstack((a,X_scaled))
test_data_120u = np.delete(a, (0), axis=1)
test_data_120u = np.reshape(test_data_120u,(72,30,25,1))



batch_size=30
nb_epoch=50
nb_filters=32
output1=32
init = "glorot_normal"


input1 = Input(shape = (30, 25, 1), name="input1")
seq1 = Convolution2D(
				nb_filters,
				nb_row=10,
				nb_col=5,
				init = init,
				border_mode = 'same',
				W_regularizer = l2( l = 0.001),
				input_shape = (30, 25, 1)
				)(input1)
seq1 = BatchNormalization(epsilon=1e-06, mode=0, momentum=0.5, weights=None)(seq1)
seq1 = Activation('relu')(seq1)

seq1 = Convolution2D(
				nb_filters,
				nb_row=5,
				nb_col=10,
				init = init,
        border_mode = "same",
				W_regularizer = l2( l = 0.001)
				)(seq1)
seq1 = BatchNormalization(epsilon=1e-06, mode=0, momentum=0.5, weights=None)(seq1)
seq1 = Activation('relu')(seq1)

seq1 = MaxPooling2D(pool_size=(2, 2), strides=None, border_mode='valid')(seq1)

seq1 = Convolution2D(
				nb_filters,
				nb_row=5,
				nb_col=5,
				init = init,
        border_mode = "same",
				W_regularizer = l2( l = 0.001)
				)(seq1)
seq1 = BatchNormalization(epsilon=1e-06, mode=0, momentum=0.5, weights=None)(seq1)
seq1 = Activation('relu')(seq1)

seq1 = Convolution2D(
				nb_filters,
				nb_row=5,
				nb_col=5,
				init = init,
        border_mode = "same",
				W_regularizer = l2( l = 0.001)
				)(seq1)
seq1 = BatchNormalization(epsilon=1e-06, mode=0, momentum=0.5, weights=None)(seq1)
seq1 = Activation('relu')(seq1)

seq1 = Convolution2D(
				nb_filters,
				nb_row=3,
				nb_col=3,
				init = init,
        border_mode = "same",
				W_regularizer = l2( l = 0.001)
				)(seq1)
seq1 = BatchNormalization(epsilon=1e-06, mode=0, momentum=0.5, weights=None)(seq1)
seq1 = Activation('relu')(seq1)

seq1 = Convolution2D(
				nb_filters,
				nb_row=3,
				nb_col=3,
				init = init,
        border_mode = "same",
				W_regularizer = l2( l = 0.001),
				activation = "relu"
				)(seq1)

seq1 = Flatten()(seq1)
output1 = Dense(output1, activation="relu")(seq1)



merged = Dense(32, activation="relu")(output1)
merged = Dense(16, activation="relu")(merged)
merged = Dense(8, activation="relu")(merged)
merged = Dense(4, activation="relu")(merged)
output = Dense(1, activation="relu",name="output")(merged)
model = Model(input=[input1],output=[output])
sgd = SGD(lr = 0.001)
adam = Adam(lr = 0.00000005)

threshold = 0
callbacks = [
    EarlyStopping(monitor='val_loss', patience=threshold, verbose=0),
]

model.compile(loss='mean_squared_error', optimizer = "adam", metrics=['mse'])

min_MSE=10000
for i in range(1000):
    history = model.fit({'input1':training_data_120u}, {'output':label_120u},
    					validation_split=0.2,
    					nb_epoch= nb_epoch, verbose = False,
    					callbacks=callbacks)
    				
    pred_u = model.predict({'input1':test_data_120u})
    from sklearn.metrics import mean_squared_error
    print("MSE: ",mean_squared_error(label_test_120u, pred_u))
    
    if(min_MSE > mean_squared_error(label_test_120u, pred_u)):
        min_MSE = mean_squared_error(label_test_120u, pred_u)
print("The best: ",min_MSE)
#np.save('cnn_u_best',pred_u)

    

