# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import glob
from scipy import ndimage
from pydicom import dcmread
import matplotlib.pyplot as plt
from skimage import morphology, color
from skimage.filters import threshold_minimum, threshold_otsu, sobel, median


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


def process(dicom_file):
    medical_image = dcmread(dicom_file)
    image = medical_image.pixel_array

    hu_image = transform_to_hu(medical_image, image)
    brain_image = window_image(hu_image, 80, 85)
    bone_image = window_image(hu_image, 230, 400)

    binary_image = bone_image > threshold_minimum(bone_image)
    edge_sobel_binary = sobel(binary_image)
    fill = ndimage.morphology.binary_fill_holes(edge_sobel_binary)
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
        'name': 'part_1_binary',
        'image': binary_image,
        'contour': None,
    })
    process.append({
        'name': 'part_1_edges',
        'image': edge_sobel_binary,
        'contour': None,
    })
    process.append({
        'name': 'part_1_fill',
        'image': fill,
        'contour': None,
    })
    process.append({
        'name': 'part_1_erosion',
        'image': erosion,
        'contour': None,
    })
    process.append({
        'name': 'part_2_otsu_binary',
        'image': otsu_image,
        'contour': None,
    })
    process.append({
        'name': 'part_2_edge_otsu',
        'image': edge_sobel_otsu,
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
