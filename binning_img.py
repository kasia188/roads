import logging
from timer_compiler import timer
import os
import numpy as np
from skimage.io import imread, imsave
from pathlib import Path

logger = logging.getLogger(__name__)

@timer
def binning(img_paths, box_size, out_folder="binned_images"):
    out_folder = Path(out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)

    binned_list = []

    for idx, path in enumerate(img_paths):
        img = imread(path)
        h, w = img.shape

        #slicing of img
        img = img[:h - h % box_size, :w - w % box_size] 
        h, w= img.shape

        binned = img.reshape(h // box_size, box_size, w // box_size, box_size).mean(axis=(1,3))

        binned = binned.astype(img.dtype)
        binned_list.append(binned)

        out_path = out_folder / f"binned_{idx}.png"
        imsave(out_path, binned)

    logger.info("Binning finished.")
    return binned_list