import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
import random
from constants import *
import imageio
import json
from dir_functions import init_annotations_dirs, init_dir, remove_dir
import concurrent.futures

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

def omit_file_extension(filename):
    number = filename.split('.')[0]
    return int(number)

def load_data(dataset_folder):
    # find paths to original images and annotations
    images_folder = os.path.join(dataset_folder, 'images')
    annotations_folder = os.path.join(dataset_folder, 'annotations')
    image_filenames = os.listdir(images_folder)
    image_filenames = sorted(image_filenames, key=omit_file_extension)

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

    print( f'{len(image_filenames)} images loaded.'   )
    start_index = omit_file_extension(image_filenames[0]) 
    return np.array(X), y, start_index

def prepare_directories():
    if CLEAR_DIRECTORIES:
        remove_dir(AUGMENTED_IMAGES_DIRECTORY)
        remove_dir(AUGMENTED_ANNOTATIONS_DIRECTORY)
        print('----------------')
    init_dir(AUGMENTED_IMAGES_DIRECTORY)
    init_annotations_dirs(AUGMENTED_ANNOTATIONS_DIRECTORY)

def augment_image_and_annotations(i, X, y, datagen, start_index):
    seed_iteration = random.randint(0, 4294967295)

    # augment and save original image
    original_image = np.expand_dims(X[i], axis=0)
    image_generator = datagen.flow(original_image, seed=seed_iteration)
    augmented_image = image_generator.next()[0]
    augmented_image = (augmented_image[:, :, 0] * 255).astype(np.uint8)
    image_save_path = os.path.join(AUGMENTED_IMAGES_DIRECTORY, f"{i}.png")
    imageio.imwrite(image_save_path, augmented_image)

    # augment and save all annotations of respective image
    for element_id, _ in y.items():
        original_annotation = np.expand_dims(y[element_id][i], axis=0)
        annotation_generator = datagen.flow(original_annotation, seed=seed_iteration)
        augmented_annotation = annotation_generator.next()[0]
        annotation_save_path = os.path.join(AUGMENTED_ANNOTATIONS_DIRECTORY, element_id, f"{i}.png")
        augmented_annotation = (augmented_annotation[:, :, 0] * 255).astype(np.uint8)
        imageio.imwrite(annotation_save_path, augmented_annotation)

def augment():
    prepare_directories()
    dataset_folder = './generated/original/'
    print('Loading dataset . . .')
    X, y, start_index = load_data(dataset_folder)
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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(augment_image_and_annotations, i, X, y, datagen, start_index) for i in range(start_index, start_index + len(X))]
        concurrent.futures.wait(futures)

# import time
# t_start = time.time()
# augment()
# t = time.time() - t_start
# print("invoices augmented in --> ", f"{t:.3f}", 'seconds', end=" ")