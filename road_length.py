import logging
from timer_compiler import timer
import numpy as np
import rasterio
from skimage.io import imread, imshow
from skimage.morphology import skeletonize, binary_closing, dilation, disk

def road_length(mask_path, tif_path):
    mask = imread(mask_path)

    if mask.ndim == 3:
        mask = mask[:, :, 0]

    mask = (mask > 127).astype(np.uint8)

    #skeleton
    skeleton = skeletonize(mask)

    skeleton_clean = binary_closing(skeleton, disk(3))
    skeleton_clean = dilation(skeleton_clean, disk(3))

    imshow(skeleton_clean)

    length_pixels = np.sum(skeleton_clean)

    #scale from GeoTIFF with rasterio
    with rasterio.open(tif_path) as src:
        pixel_size = src.res[0] #m/pixel

    length_meters = length_pixels * pixel_size

    return length_meters