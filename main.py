import cv2
import numpy as np
from skimage import io

# sample_imgs/1.jpg
# https://i.stack.imgur.com/DNM65.png

img_url = 'sample_imgs/3.jpg'
imgs = [
    'sample_imgs/1.jpg',
    'sample_imgs/2.png',
    'sample_imgs/3.jpg',
    'sample_imgs/3.png',
]

for url in imgs:
    if url.split(".")[-1] == "jpg":
        img = io.imread(url)[:, :, :]
    else:
        img = io.imread(url)[:, :, :-1]

    # print(img)
    # exit()

    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]

    # print(url)
    print(url)
    print(str(round(dominant[0])) + "," + str(round(dominant[1]))
          + "," + str(round(dominant[2])))
    print('\n')
