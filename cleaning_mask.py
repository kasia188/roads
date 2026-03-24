from timer_compiler import timer
import logging
import numpy as np
from skimage.morphology import remove_small_objects, disk, closing
from scipy.ndimage import binary_fill_holes
from skimage.io import imsave
from pathlib import Path

logger = logging.getLogger(__name__)

@timer
def clean_mask(masks, size_1, size_2, disk_size, out_folder=None):
    cleaned_masks = []

    if out_folder is not None:
        out_folder = Path(out_folder)
        out_folder.mkdir(parents=True, exist_ok=True)

    for i, mask in enumerate(masks):

        if mask.ndim == 3:
            mask = mask[:, :, 0]

        mask_bool = mask > 127

        mask_clean = remove_small_objects(mask_bool, max_size=size_1)
        mask_clean = binary_fill_holes(mask_clean)
        mask_clean = remove_small_objects(mask_clean, max_size=size_2)
        mask_clean = closing(mask_clean, disk(disk_size))

        mask_clean = (mask_clean.astype(np.uint8)) * 255
        cleaned_masks.append(mask_clean)

        if out_folder is not None:
            filename = out_folder / f"mask_cleaned_{i}.png"
            imsave(filename, mask_clean)
            
    return cleaned_masks