
import numpy as np
import matplotlib.pyplot as plt
import cv2, os

import tensorflow as tf
import keras
import sys
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from keras.losses import categorical_crossentropy
from keras.optimizers import adam, sgd
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from keras.models import Model
from keras.applications.mobilenet_v2 import MobileNetV2

from PIL import Image
dataset_path = sys.argv[1]



train_path = os.path.join(dataset_path, 'train')
test_path = os.path.join(dataset_path, 'test')
IMG_BREDTH = 30
IMG_HEIGHT = 60
num_classes = 4
img_size = 128
now_path = os.getcwd()

def get_dataset():

	train_batch = ImageDataGenerator(featurewise_center=True,
									 featurewise_std_normalization=True,
	                                 samplewise_center=False, 
	                                 samplewise_std_normalization=False, 
	                                 zca_whitening=False, 
	                                 rotation_range=45, 
	                                 width_shift_range=0.2, 
	                                 height_shift_range=0.2, 
	                                 horizontal_flip=True, 
	                                 vertical_flip=False).flow_from_directory(train_path, 
	                                                                          target_size=(img_size, img_size), 
	                                                                          classes=['o', 'R', 'P', 'other'], 
	                                                                          batch_size=40)

	test_batch = ImageDataGenerator().flow_from_directory(test_path, 
	                                                      target_size=(img_size, img_size), 
														  classes=['o', 'R', 'P', 'other'], 
	                                                      batch_size=40)
	return train_batch, test_batch
# def cnn_model():
    
#     model = Sequential()

#     model.add(Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu', input_shape=(IMG_HEIGHT,IMG_BREDTH,3)))
#     model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
#     model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.25))

#     model.add(Conv2D(img_size, kernel_size=(3, 3), activation='relu'))
#     model.add(Conv2D(img_size, kernel_size=(3, 3), activation='relu'))
#     model.add(Conv2D(img_size, kernel_size=(3, 3), activation='relu'))
#     model.add(Dropout(0.25))
    
#     model.add(Flatten())

#     model.add(Dense(512, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(512, activation='relu'))
#     model.add(Dropout(0.5))

#     model.add(Dense(num_classes, activation='softmax'))
              
#     model.summary()
              
#     return model

def use_model(path):
    model = load_model(os.path.join(now_path, 'Waste-classification', 'best_waste_classifier.h5'))
    # pic = plt.imread(path)
    pic = cv2.imread(path)
    pic = cv2.resize(pic, (img_size, img_size))
    pic = np.expand_dims(pic, axis=0)
    classes = model.predict(pic)
    
#     code using PIL
#     model = load_model('best_waste_classifier.h5')
#     pic1 = plt.imread(path)
#     pic = Image.open(path).resize((IMG_BREDTH, IMG_HEIGHT))
#     plt.imshow(pic1)
#     if model.predict_classes(np.expand_dims(pic, axis=0)) == 0:
#         classes = 'ORGANIC'
#     elif model.predict_classes(np.expand_dims(pic, axis=0)) == 1:
#         classes = 'RECYCLABLE'
    idx_class = classes.index(max(classes))
    if idx_class == 1:
    	return 'RECYCLABLE'
    else:
    	return 'NON_RECYCLABLE'

base_model = MobileNetV2(input_shape=(img_size, img_size, 3), alpha=1.0, include_top=False, weights='imagenet', input_tensor=None, pooling=None, classes=4)

train_batch, test_batch = get_dataset()

x=base_model.output
flat_x = Flatten()(x)
classification_output = Dense(4, activation = 'softmax', name='output_d')(flat_x)

model=Model(inputs=base_model.input,outputs=classification_output)

checkpoint = ModelCheckpoint(os.path.join(now_path, 'Waste-classification', 'best_waste_classifier.h5'), 
                             monitor='val_loss', 
                             verbose=0, 
                             save_best_only=True, 
                             mode='auto')
model.compile(loss='categorical_crossentropy', optimizer=adam(lr=1.0e-4), metrics=['accuracy'])

model = model.fit_generator(train_batch,  
                        validation_data=test_batch,  
                        epochs=30, 
                        steps_per_epoch=len(train_batch),
                        verbose=1, 
                        validation_steps=len(test_batch),
                        callbacks=[checkpoint])

# run code to train the neural network

print(len(train_batch))
# use_model('/home/yiwang454/Waste-classification/test_orange.jpg')

use_model(os.path.join(now_path, 'Waste-classification', 'test_orange.jpg'))