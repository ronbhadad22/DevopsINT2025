import numpy as np
from PIL import Image


def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


def open_img(img_path):
    # Open image using PIL and convert to numpy array
    img = np.array(Image.open(img_path))
    # Convert to grayscale if RGB
    if len(img.shape) > 2 and img.shape[2] >= 3:
        return rgb2gray(img).tolist()
    return img.tolist()


def save_img(img, filename):
    # Convert list back to numpy array if needed
    if isinstance(img, list):
        img = np.array(img)
    # Save using PIL
    Image.fromarray(np.uint8(img)).save(filename)
