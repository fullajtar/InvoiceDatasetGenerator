import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
import random
from constants import *
import imageio
import json

def add_noise(img):
    '''Add random noise to an image'''
    VARIABILITY = 20
    deviation = VARIABILITY * tf.random.uniform(shape=(), minval=0, maxval=1)
    noise = tf.random.normal(shape=tf.shape(img), mean=0, stddev=deviation, dtype=tf.float32)
    img += noise
    img = tf.clip_by_value(img, 0.0, 255.0)
    return img

def init_annotations_dictionary():
    with open(FIELD_INCLUSION, 'r', encoding='utf-8') as file:
        fields_dict = json.load(file)
        for element_id, _ in fields_dict.items():
            fields_dict[element_id] = []
    return fields_dict

def load_data(dataset_folder):
    # find paths to original images and annotations
    images_folder = os.path.join(dataset_folder, 'images')
    annotations_folder = os.path.join(dataset_folder, 'annotations')
    image_filenames = os.listdir(images_folder)

    X = []
    y = init_annotations_dictionary()

    for image_filename in image_filenames:
        img_path = os.path.join(images_folder, image_filename)
        annotation_path = os.path.join(annotations_folder, 'address_text', image_filename)

        # Load and preprocess the image
        img = load_img(img_path, target_size=(ORIGINAL_HEIGHT, ORIGINAL_WIDTH), color_mode='grayscale')
        img_array = img_to_array(img) / 255.0  # Normalize pixel values
        X.append(img_array)

        # load and preprocess all annotations of respective image
        for element_id, _ in y.items():
            annotation_path = os.path.join(annotations_folder, element_id, image_filename)
            annotation = load_img(annotation_path, target_size=(ORIGINAL_HEIGHT, ORIGINAL_WIDTH), color_mode='grayscale')
            annotation_array = img_to_array(annotation) / 255.0  # Normalize pixel values
            y[element_id].append(annotation_array)

    for element_id, annotation_list in y.items():
        y[element_id] = np.array(annotation_list) 

    return np.array(X), y

def augment():
    dataset_folder = './generated/original/'
    print('Loading dataset . . .')
    X, y = load_data(dataset_folder)
    print('Augmenting . . .')

    # Create an ImageDataGenerator
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.05,
        height_shift_range=0.05,
        shear_range=0.1,
        zoom_range=0.2,
        horizontal_flip=False,
        fill_mode='nearest'
    )

    # Iterate over the images and annotations simultaneously
    for i in range(len(X)):

        # generate seed to secure identical augments of file and annotations
        seed_iteration = random.randint(0, 4294967295)

        # augment and save original image
        original_image = np.expand_dims(X[i], axis=0)
        image_generator = datagen.flow(original_image, seed=seed_iteration)
        augmented_image = image_generator.next()[0]
        # augmented_image = add_noise(augmented_image)
        augmented_image = (augmented_image[:, :, 0] * 255).astype(np.uint8)
        image_save_path = os.path.join(AUGMENTED_IMAGES_DIRECTORY, f"{i}.png")
        imageio.imwrite(image_save_path, augmented_image)

        # augment and save all annotations of respective image
        for element_id, _ in y.items():
            original_annotation = np.expand_dims(y[element_id][i], axis=0)
            annotation_generator = datagen.flow(original_annotation, seed=seed_iteration)
            augmented_annotation = annotation_generator.next()[0]
            annotation_save_path = os.path.join(AUGMENTED_LABELS_DIRECTORY, element_id, f"{i}.png")
            augmented_annotation = (augmented_annotation[:, :, 0] * 255).astype(np.uint8)
            imageio.imwrite(annotation_save_path, augmented_annotation)

# augment() #for debug only, if uncommented augmentation will be called 2 times