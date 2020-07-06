# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import glob
from scipy import ndimage
from pydicom import dcmread
import matplotlib.pyplot as plt
from skimage import morphology, color, segmentation
from skimage.filters import threshold_minimum, threshold_otsu, sobel, median
from skimage.measure import regionprops


def transform_to_hu(medical_image, image):
    intercept = medical_image.RescaleIntercept
    slope = medical_image.RescaleSlope
    hu_image = image * slope + intercept

    return hu_image


def window_image(image, window_center, window_width):
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    window_image = image.copy()
    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max

    return window_image


def savefig(image, processname, filename, contour=None):
    dirname = os.path.splitext(filename)[0]
    try:
        os.makedirs(dirname)
    except OSError as e:
        pass

    full_path = os.path.join(dirname, '{}.jpeg'.format(processname))

    plt.figure()
    plt.style.use('grayscale')
    plt.imshow(image)
    if contour is not None:
        plt.contour(contour, colors='red', linewidths=1)
    plt.title(processname)
    plt.axis('off')

    plt.savefig(full_path)
    plt.clf()

    return full_path


def get_center(sample, image):
    labeled_foreground = sample.astype(int)
    properties = regionprops(labeled_foreground, image)
    center_of_mass = properties[0].centroid
    # weighted_center_of_mass = properties[0].weighted_centroid

    return (int(center_of_mass[0]), int(center_of_mass[1]))


def process(dicom_file):
    medical_image = dcmread(dicom_file)
    image = medical_image.pixel_array

    hu_image = transform_to_hu(medical_image, image)
    brain_image = window_image(hu_image, 80, 85)
    bone_image = window_image(hu_image, 230, 230)

    binary_image = bone_image > threshold_minimum(bone_image)
    edge_sobel_binary = sobel(binary_image)
    fill = segmentation.flood_fill(
        edge_sobel_binary, get_center(brain_image, image), 255)
    erosion = morphology.erosion(fill, morphology.disk(30))

    otsu_image = brain_image > threshold_otsu(brain_image)
    edge_sobel_otsu = sobel(otsu_image)

    multiplication_images = erosion * edge_sobel_otsu
    mediam_filter = median(multiplication_images)

    process = []
    process.append({
        'name': 'original_image',
        'image': brain_image,
        'contour': None,
    })

    process.append({
        'name': 'part_1_otsu_binary',
        'image': otsu_image,
        'contour': None,
    })
    process.append({
        'name': 'part_1_edge_otsu',
        'image': edge_sobel_otsu,
        'contour': None,
    })

    process.append({
        'name': 'part_2_binary',
        'image': binary_image,
        'contour': None,
    })
    process.append({
        'name': 'part_2_edges',
        'image': edge_sobel_binary,
        'contour': None,
    })
    process.append({
        'name': 'part_2_fill',
        'image': fill,
        'contour': None,
    })
    process.append({
        'name': 'part_2_erosion',
        'image': erosion,
        'contour': None,
    })

    process.append({
        'name': 'multiplication_images',
        'image': multiplication_images,
        'contour': None,
    })
    process.append({
        'name': 'mediam_filters',
        'image': mediam_filter,
        'contour': None,
    })

    process.append({
        'name': 'segmentation',
        'image': brain_image,
        'contour': mediam_filter
    })

    return process


def process_and_save(_filename):
    fig_paths = []
    for processed_files in process(_filename):
        fig_paths.append(savefig(
            image=processed_files['image'],
            processname=processed_files['name'],
            contour=processed_files['contour'],
            filename=_filename,
        ))
    plt.close('all')
    return fig_paths
