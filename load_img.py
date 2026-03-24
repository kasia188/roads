import logging
from timer_compiler import timer
from pathlib import Path
from skimage.io import imread
from skimage.color import rgb2hsv

logger = logging.getLogger(__name__)

@timer
def load_img(folder):
    rgb_folder = Path(folder)       #zmieniamy string rgb_folder na obiekt Path

    if not rgb_folder.exists():
        logger.warning(f"No folder named {rgb_folder}.")
        return []
    
    rgb_paths = sorted(rgb_folder.glob("*.tiff"))
    
    if not rgb_paths:
        logger.warning(f"No .tiff files in folder named {rgb_folder}.")

    return rgb_paths

@timer
def channels(paths_folder, channel):
    if channel not in "rgbhsv":
        logger.warning(f"No such channel found: {channel}")
        return[]

    rgb = {"r" : 0, "g" : 1, "b" : 2}
    hsv = {"h" : 0, "s" : 1, "v" : 2}
    
    result = []

    for path in paths_folder:
        img = imread(path)

        if channel in rgb:
            ch_img = img[:, :, rgb[channel]]
        else:
            hsv_img = rgb2hsv(img)
            ch_img = hsv_img[:, :, hsv[channel]]
            
        result.append(ch_img)
    
    return result