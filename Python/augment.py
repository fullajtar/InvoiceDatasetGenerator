import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
# import tensorflow_datasets as tfds
import os
import random
import numpy as np

from tensorflow.keras import layers
from constants import *
import json
import re
import time
from bs4 import BeautifulSoup
from faker import Faker
from datetime import datetime, timedelta
from FakeClass import FakeClass
from constants import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tensorflow.keras.preprocessing.image import save_img

from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array

# SOURCES: https://www.tensorflow.org/tutorials/images/data_augmentation
# https://pytorch.org/vision/main/transforms.html

RESCALE_CONSTANT = 1
ORIGINAL_HEIGHT, ORIGINAL_WIDTH = 1153, 821
CROP_RESCALE_CONSTANT = 1
TRANSLATION_RESCALE_CONSTANT = 1
IMG_HEIGHT, IMG_WIDTH = int(ORIGINAL_HEIGHT * RESCALE_CONSTANT), int(ORIGINAL_WIDTH * RESCALE_CONSTANT)

# def add_noise(img):
#     '''Add random noise to an image'''
#     VARIABILITY = 25
#     deviation = VARIABILITY*random.random()
#     noise = np.random.normal(0, deviation, img.shape)
#     img += noise
#     np.clip(img, 0., 255.)
#     return img

def add_noise(img):
    '''Add random noise to an image'''
    VARIABILITY = 20
    deviation = VARIABILITY * tf.random.uniform(shape=(), minval=0, maxval=1)
    noise = tf.random.normal(shape=tf.shape(img), mean=0, stddev=deviation, dtype=tf.float32)
    img += noise
    img = tf.clip_by_value(img, 0.0, 255.0)
    return img

def get_augment_model():
    augment_model = tf.keras.Sequential([
        layers.Resizing(IMG_HEIGHT, IMG_WIDTH ),
        layers.RandomCrop(int(ORIGINAL_HEIGHT * CROP_RESCALE_CONSTANT), int(ORIGINAL_WIDTH * CROP_RESCALE_CONSTANT)),  # Cropping
        layers.RandomRotation(0.01, fill_mode = "constant", fill_value = 255),
        layers.RandomZoom(height_factor = (0.05 ,0.2), fill_mode = "constant", fill_value = 255),  # Scaling (random zoom)
        layers.RandomTranslation((-0.05, 0.05),(-0.05, 0.05), fill_mode = "constant", fill_value = 255),  # Translation
        # layers.Lambda(lambda x: tf.image.random_saturation(x, 0.5, 1.5)),  # Additional augmentation (e.g., saturation)
        layers.Lambda(lambda x: tf.image.random_contrast(x, 0.8, 1.2)),  # Additional augmentation (e.g., contrast)
        layers.Lambda(lambda x: tf.image.random_brightness(x, 0.1)),  # Additional augmentation (e.g., brightness)
        # layers.Conv2D(filters=3, kernel_size=(3, 3), activation='relu', padding='same'),  # Example layer after augmentation
        # layers.GaussianNoise(0.8),  # Noise injection
    ])
    return augment_model

# Define a function to read and preprocess an image

def augment():
    data_augmentation = get_augment_model()
    def load_and_preprocess_image(file_path):
        rgb_image = tf.io.read_file(file_path)
        rgb_image = tf.image.decode_png(rgb_image, channels=3)
        grayscale_image = tf.image.rgb_to_grayscale(rgb_image)
        augmented_image = data_augmentation(grayscale_image)
        augmented_image = add_noise(augmented_image)
        return augmented_image
    # Get a list of all file paths in the folder
    file_paths = [os.path.join(OUT_DIRECTORY, file) for file in os.listdir(OUT_DIRECTORY)]

    # Create a dataset of file paths
    file_paths_dataset = tf.data.Dataset.from_tensor_slices(file_paths)

    # Map the function over the dataset to load and preprocess all images
    images_dataset = file_paths_dataset.map(load_and_preprocess_image)

    for i, image in enumerate(images_dataset):
        os.makedirs(AUGMENTED_IMAGES_DIRECTORY, exist_ok=True)
        file_path = os.path.join(AUGMENTED_IMAGES_DIRECTORY, f'augmented_image_{i}.png')
        save_img(file_path, image.numpy())

augment()

# def augment_single_image(image_path):

#     Create an iterator from the dataset
#     iterator = iter(images_dataset)
#     sample_image = next(iterator)
#     sample_image_np = sample_image.numpy()
#     if sample_image_np.shape[-1] == 1:
#         sample_image_np = sample_image_np[:, :, 0]
#     plt.imshow(sample_image_np, cmap='gray')
#     plt.axis('off')  # Turn off axis labels
#     plt.show()

#     # Load the image
#     # image_path = './generated_images/0.png'
#     rgb_image = tf.io.read_file(image_path)
#     rgb_image = tf.image.decode_png(rgb_image, channels=3)
#     image = tf.image.rgb_to_grayscale(rgb_image)

#     augmented_image = data_augmentation(image)
#     augmented_image = add_noise(augmented_image)
#     save_path = os.path.join(AUGMENTED_IMAGES_DIRECTORY, f'augmented_image_{i}.png')
#     plt.imsave(save_path, tf.squeeze(augmented_image, axis=-1), cmap='gray', format='png')