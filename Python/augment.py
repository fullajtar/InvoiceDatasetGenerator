import tensorflow as tf
import os

from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import save_img
from constants import *

# SOURCES: 
    # https://www.tensorflow.org/tutorials/images/data_augmentation
    # https://pytorch.org/vision/main/transforms.html
    # https://stackoverflow.com/a/61425288

RESCALE_CONSTANT = 1
ORIGINAL_HEIGHT, ORIGINAL_WIDTH = 1153, 821
CROP_RESCALE_CONSTANT = 1
TRANSLATION_RESCALE_CONSTANT = 1
IMG_HEIGHT, IMG_WIDTH = int(ORIGINAL_HEIGHT * RESCALE_CONSTANT), int(ORIGINAL_WIDTH * RESCALE_CONSTANT)

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
        layers.Lambda(lambda x: tf.image.random_contrast(x, 0.8, 1.2)),  # Additional augmentation (e.g., contrast)
        layers.Lambda(lambda x: tf.image.random_brightness(x, 0.1)),  # Additional augmentation (e.g., brightness)

        # unusable for grayscale
        # layers.Lambda(lambda x: tf.image.random_saturation(x, 0.5, 1.5)),  # Additional augmentation (e.g., saturation)
        # layers.Conv2D(filters=3, kernel_size=(3, 3), activation='relu', padding='same'),  # Example layer after augmentation

        # was not sufficient
        # layers.GaussianNoise(0.8),  # Noise injection
    ])
    return augment_model

def augment():
    data_augmentation = get_augment_model()

    # function to read and augment an image
    # have to be inside augment() to access data_augmentation without lambda usage
    def load_and_augment_image(file_path):
        rgb_image = tf.io.read_file(file_path)
        rgb_image = tf.image.decode_png(rgb_image, channels=3)
        grayscale_image = tf.image.rgb_to_grayscale(rgb_image)
        augmented_image = data_augmentation(grayscale_image)
        augmented_image = add_noise(augmented_image)
        return augmented_image
    
    # get a list of all file paths in the folder
    file_paths = [os.path.join(OUT_DIRECTORY, file) for file in os.listdir(OUT_DIRECTORY)]
    # create a dataset of file paths
    file_paths_dataset = tf.data.Dataset.from_tensor_slices(file_paths)
    # Map the function over the dataset to load and augment all images
    images_dataset = file_paths_dataset.map(load_and_augment_image)

    os.makedirs(AUGMENTED_IMAGES_DIRECTORY, exist_ok=True)
    for i, image in enumerate(images_dataset):
        file_path = os.path.join(AUGMENTED_IMAGES_DIRECTORY, f'augmented_image_{i}.png')
        save_img(file_path, image.numpy())

# augment() #augment debug only