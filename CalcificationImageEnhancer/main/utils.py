import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from tkinter import *

from keras.models import load_model
from PIL import Image, ImageTk, ImageOps



filename = ""
minVal = 135
maxVal = 155

img_height, img_width = (224,224)


def rearrange(result_img):
    if result_img.shape == 3:
        blue,green,red = cv2.split(result_img)
        result_img = cv2.merge((red,green,blue))
    arranged_img = Image.fromarray(result_img)
    return arranged_img

def resize(arranged_img):
    resized_img= arranged_img.resize((300,350), Image.LANCZOS)
    final_img = ImageTk.PhotoImage(resized_img)
    return final_img

def equalize(img):
    equalized_img = cv2.equalizeHist(img)
    return equalized_img

def predict(imageIn):
    imageIn = (rearrange(imageIn))
    # Load the model
    model = load_model("main/mammo-caps-model/keras_model.h5", compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(imageIn, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(str(prediction)+" FROM: predict()")

    # concat and return
    num1 = prediction[0,0]
    num2 = prediction[0,1]
    num3 = prediction[0,2]
    
    return num1, num2, num3

