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
            fields_dict[element_id] = {}
    return fields_dict

def omit_file_extension(filename):
    number = filename.split('.')[0]
    return int(number)

def load_and_preprocess_image(image_filename, images_folder, annotations_folder, X, y):
    img_path = os.path.join(images_folder, image_filename)
    annotation_path = os.path.join(annotations_folder, 'address_text', image_filename)
    image_number = omit_file_extension(image_filename)

    # Load and preprocess the image
    img = load_img(img_path, target_size=(ORIGINAL_HEIGHT, ORIGINAL_WIDTH), color_mode='grayscale')
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    X[image_filename] = img_array

    # load and preprocess all annotations of respective image
    for element_id, _ in y.items():
        annotation_path = os.path.join(annotations_folder, element_id, image_filename)
        if not os.path.isfile(annotation_path):
            print(f"The file '{annotation_path}' was not found.")
            raise FileNotFoundError(f"The file '{annotation_path}' was not found.")
        annotation = load_img(annotation_path, target_size=(ORIGINAL_HEIGHT, ORIGINAL_WIDTH), color_mode='grayscale')
        annotation_array = img_to_array(annotation) / 255.0  # Normalize pixel values
        y[element_id][image_filename] = annotation_array

def init_seed_for_imagename(image_filenames) -> dict:
    seed_dict = {}
    for image_filename in image_filenames:
        seed_dict[image_filename] = random.randint(0, 4294967295)
    return seed_dict

def load_data(dataset_folder):
    # find paths to original images and annotations
    images_folder = os.path.join(dataset_folder, 'images')
    annotations_folder = os.path.join(dataset_folder, 'annotations')
    image_filenames = os.listdir(images_folder)
    image_filenames = sorted(image_filenames, key=omit_file_extension)

    X = {}
    y = init_annotations_dictionary()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(load_and_preprocess_image, image_filename, images_folder, annotations_folder, X, y) for image_filename in image_filenames]
        concurrent.futures.wait(futures)

    print( f'{len(image_filenames)} images loaded.'   )
    return X, y, image_filenames

def prepare_directories():
    if CLEAR_DIRECTORIES:
        remove_dir(AUGMENTED_IMAGES_DIRECTORY)
        remove_dir(AUGMENTED_ANNOTATIONS_DIRECTORY)
        print('----------------')
    init_dir(AUGMENTED_IMAGES_DIRECTORY)
    init_annotations_dirs(AUGMENTED_ANNOTATIONS_DIRECTORY)

def augment_annotations(image_filename, X, y, datagen, seed_iteration):
    for element_id, _ in y.items():
        print(f'annotation seed: {seed_iteration} {image_filename}')
        original_annotation = np.expand_dims(np.array(y[element_id][image_filename]), axis=0)
        annotation_generator = datagen.flow(original_annotation, seed=seed_iteration)
        augmented_annotation = annotation_generator.next()[0]
        annotation_save_path = os.path.join(AUGMENTED_ANNOTATIONS_DIRECTORY, element_id, f"{image_filename}")
        augmented_annotation = (augmented_annotation[:, :, 0] * 255).astype(np.uint8)
        imageio.imwrite(annotation_save_path, augmented_annotation)

def augment_image_and_annotations(image_filename, X, y, datagen, seed_iteration):

    # augment and save original image
    original_image = np.expand_dims(np.array(X[image_filename]), axis=0)
    image_generator = datagen.flow(original_image, seed=seed_iteration)
    augmented_image = image_generator.next()[0]
    augmented_image = (augmented_image[:, :, 0] * 255).astype(np.uint8)
    image_save_path = os.path.join(AUGMENTED_IMAGES_DIRECTORY, f"{image_filename}")
    imageio.imwrite(image_save_path, augmented_image)

    # augment and save all annotations of respective image
    for element_id, _ in y.items():
        original_annotation = np.expand_dims(np.array(y[element_id][image_filename]), axis=0)
        annotation_generator = datagen.flow(original_annotation, seed=seed_iteration)
        augmented_annotation = annotation_generator.next()[0]
        annotation_save_path = os.path.join(AUGMENTED_ANNOTATIONS_DIRECTORY, element_id, f"{image_filename}")
        augmented_annotation = (augmented_annotation[:, :, 0] * 255).astype(np.uint8)
        imageio.imwrite(annotation_save_path, augmented_annotation)

def augment():
    prepare_directories()
    dataset_folder = './generated/original/'
    print('Loading dataset . . .')
    X, y, image_filenames = load_data(dataset_folder)
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

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(augment_image_and_annotations, image_filename, X, y, datagen, seed) for image_filename, seed in image_filenames.items()]
    #     concurrent.futures.wait(futures)

    for image_filename in image_filenames:
        augment_image_and_annotations(image_filename, X, y, datagen, random.randint(0, 4294967295))

# import time
# t_start = time.time()
# augment()
# t = time.time() - t_start
# print("invoices augmented in --> ", f"{t:.3f}", 'seconds', end=" ")