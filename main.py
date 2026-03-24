from logger_compiler import setup_logger
from load_img import load_img, channels
from cleaning_mask import clean_mask
from binning_img import binning
import numpy as np
from pathlib import Path
import logging
from skimage.io import imsave
from road_length import road_length

logger = logging.getLogger(__name__)

def main():
    setup_logger()

    folder  = r"C:\Users\katar\roads2\data_test"
    rgb_paths = load_img(folder)

    s_channels = channels(rgb_paths, "s")

    temp_s_folder = Path("temp_s_3")
    temp_s_folder.mkdir(exist_ok=True)
    logger.info(f"Temp folder: {temp_s_folder.resolve()}")

    temp_paths = []
    for i, s in enumerate(s_channels):
        path = temp_s_folder / f"s_channel_{i}.png"
        # zapisujemy jako 0-255
        imsave(path, (s * 255).astype(np.uint8))
        temp_paths.append(path)
        logger.info(f"image {i} in folder temp_paths")

    binned_s_list = []
    binned_s_list = binning(temp_paths, box_size=6)

    masks = []
    for s_binned in binned_s_list:
        mask = np.zeros_like(s_binned, dtype=np.uint8)
        mask[s_binned < 20] = 255
        masks.append(mask)

    clean_mask(masks, size_1=500, size_2=3000, disk_size=2, out_folder="cleaned_masks_3")
    logger.info("Masks cleaned.")

    
if __name__ == "__main__":
    main()