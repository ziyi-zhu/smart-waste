import numpy as np
import matplotlib.pyplot as plt
import cv2

import tensorflow as tf
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from keras.losses import categorical_crossentropy
from keras.optimizers import adam, sgd
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

import serial

from PIL import Image

def use_model(frame):
	model = load_model('model1.h5')
	# frame = plt.imread('waste.jpg')
	pic = cv2.resize(frame, (30, 60))
	pic = np.expand_dims(pic, axis=0)
	classes = model.predict_classes(pic)
	
#     code using PIL
#     model = load_model('best_waste_classifier.h5')
#     pic1 = plt.imread(path)
#     pic = Image.open(path).resize((IMG_BREDTH, IMG_HEIGHT))
#     plt.imshow(pic1)
#     if model.predict_classes(np.expand_dims(pic, axis=0)) == 0:
#         classes = 'ORGANIC'
#     elif model.predict_classes(np.expand_dims(pic, axis=0)) == 1:
#         classes = 'RECYCLABLE'
	
	return classes

ser = serial.Serial('COM5', 9600)

while True:
	if(ser.in_waiting > 0):
		line = ser.readline()

		cap = cv2.VideoCapture(1) # video capture source camera (Here webcam of laptop) 
		ret,frame = cap.read() # return a single frame in variable `frame`

		predict = use_model(frame)[0]

		cv2.imwrite('waste.jpg', frame)

		if predict == 0:
			ser.write(b'u')
		else:
			ser.write(b'd')