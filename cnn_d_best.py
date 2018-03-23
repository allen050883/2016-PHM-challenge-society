import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math as m
import keras as k
from sklearn import preprocessing
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, merge, Input, Activation
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.pooling import GlobalAveragePooling2D
from keras.utils import np_utils
from keras.regularizers import l1l2, activity_l2, l2, l1
from keras.optimizers import SGD, Adadelta, Adam
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping

path = '/home/someone/桌面/project3_cnn'
training_data_120d = np.load(str(path)+'/training_data_120d_roll10_best.npy')
test_data_120d = np.load(str(path)+'/test_data_120d_roll10_best.npy')
label_120d = np.load(str(path)+'/label_120d_roll10_best.npy')
label_120d = label_120d[:,2]
label_test_120d = np.load(str(path)+'/label_test_120d_roll10_best.npy')
label_test_120d = label_test_120d[:,2]



'''scaling'''
'''
training_data_120d = np.reshape(training_data_120d,(45185,59))
a= np.zeros((45185, 1))
for i in range(training_data_120d.shape[1]):
    X_scaled = preprocessing.scale(training_data_120d[:,i])
    X_scaled = np.reshape(X_scaled,(45185,1))
    a = np.hstack((a,X_scaled))
training_data_120d = np.delete(a, (0), axis=1)
training_data_120d = np.reshape(training_data_120d,(1291,35,59,1))


test_data_120d = np.reshape(test_data_120d,(11270,59))
a= np.zeros((11270, 1))
for i in range(test_data_120d.shape[1]):
    X_scaled = preprocessing.scale(test_data_120d[:,i])
    X_scaled = np.reshape(X_scaled,(11270,1))
    a = np.hstack((a,X_scaled))
test_data_120d = np.delete(a, (0), axis=1)
test_data_120d = np.reshape(test_data_120d,(322,35,59,1))
'''


batch_size=30
nb_epoch=50
nb_filters=32
output1=32
init = "glorot_normal"


input1 = Input(shape = (35, 59, 1), name="input1")
seq1 = Convolution2D(
				nb_filters,
				nb_row=7,
				nb_col=7,
				init = init,
				border_mode = 'same',
				W_regularizer = l2( l = 0.001),
				input_shape = (35, 59, 1)
				)(input1)
seq1 = BatchNormalization(epsilon=1e-03, mode=0, momentum=0.5, weights=None)(seq1)
seq1 = Activation('relu')(seq1)

seq1 = Convolution2D(
				nb_filters,
				nb_row=5,
				nb_col=5,
				init = init,
				border_mode = "same",
				W_regularizer = l2( l = 0.001)
				)(seq1)
seq1 = BatchNormalization(epsilon=1e-03, mode=0, momentum=0.5, weights=None)(seq1)
seq1 = Activation('relu')(seq1)
seq1 = MaxPooling2D(pool_size=(2, 2), strides=None, border_mode='valid')(seq1)

seq1 = Flatten()(seq1)
output1 = Dense(output1, activation="relu")(seq1)



merged = Dense(64, activation="relu")(output1)
merged = Dense(32, activation="relu")(merged)
merged = Dense(16, activation="relu")(merged)
output = Dense(1, activation="relu",name="output")(merged)
model = Model(input=[input1],output=[output])
sgd = SGD(lr = 0.001)
adam = Adam(lr = 0.0000001)

threshold = 5
callbacks = [
    EarlyStopping(monitor='val_loss', patience=threshold, verbose=0),
]

model.compile(loss='mean_squared_error', optimizer = "adam", metrics=['mse'])

min_MSE = 10000
for i in range(5):
    history = model.fit({'input1':training_data_120d}, {'output':label_120d},
    					validation_split=0.2,
    					nb_epoch= nb_epoch, verbose = True, 
    					callbacks=callbacks)
    
    pred_d = model.predict({'input1':test_data_120d})
    from sklearn.metrics import mean_squared_error
    print("MSE: ",mean_squared_error(label_test_120d, pred_d))
    if(min_MSE > mean_squared_error(label_test_120d, pred_d)):
        min_MSE = mean_squared_error(label_test_120d, pred_d)
print("The best: ",min_MSE)
np.save('cnn_d_best',pred_d)
