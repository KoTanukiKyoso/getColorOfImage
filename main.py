import cv2
import numpy as np
from skimage import io
from skimage import color

colors = {
    "red": {
        "name": "red", "ja": "赤",
        "r": 255, "g": 0, "b": 0,
    },
    "yellow": {
        "name": "yellow", "ja": "黄",
        "r": 255, "g": 255, "b": 0,
    },
    "orange": {
        "name": "orange", "ja": "橙",
        "r": 255, "g": 165, "b": 0,
    },
    "blue": {
        "name": "blue", "ja": "青",
        "r": 0, "g": 0, "b": 255,
    },
    "green": {
        "name": "green", "ja": "緑",
        "r": 0, "g": 128, "b": 0,
    },
    "indigo": {
        "name": "indigo", "ja": "藍",
        "r": 22, "g": 94, "b": 131,
    },
    "purple": {
        "name": "purple", "ja": "紫",
        "r": 128, "g": 0, "b": 128,
    },
    # 水色　等検証
    "black": {
        "name": "black", "ja": "黒",
        "r": 0, "g": 0, "b": 0,
    },
    "white": {
        "name": "white", "ja": "白",
        "r": 255, "g": 255, "b": 255,
    },
    "grey": {
        "name": "grey", "ja": "灰",
        "r": 128, "g": 128, "b": 128,
    },
}


def skimage_rgb2lab(rgb):
    return color.rgb2lab(rgb.reshape(1, 1, 3))


def compare_color(c1, c2):
    return color.deltaE_ciede2000(skimage_rgb2lab(c1), skimage_rgb2lab(c2))


def get_colors(_url):
    if _url.split(".")[-1] == "jpg":
        img = io.imread(_url)[:, :, :]
    else:
        img = io.imread(_url)[:, :, :-1]

    pixels = np.float32(img.reshape(-1, 3))
    n_colors = 4
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    # dominant = palette[np.argmax(counts)]
    color_list = {}
    for _color in palette:
        # print(str(round(_color[0])) + "," + str(round(_color[1]))
        #       + "," + str(round(_color[2])))
        for cs in colors.values():
            color1 = np.array([cs["r"], cs["g"], cs["b"]], np.uint8)
            color2 = np.array([_color[0], _color[1], _color[2]], np.uint8)
            dif = compare_color(color1, color2)
            if dif < 24:
                # print(_url + ":" + cs["ja"] + ":" + str(dif))
                color_list[cs["ja"]] = cs["ja"]

    _list = ""
    for _color in color_list:
        _list += _color + " "

    return _list


images = [
    # 'sample_imgs/1.jpg',
    'sample_imgs/2.png',
    # 'sample_imgs/3.jpg',
    'sample_imgs/3.png',
    'sample_imgs/4.jpg',
    'sample_imgs/5.jpg',
    'sample_imgs/6.jpg',
    'sample_imgs/7.jpg',
    'sample_imgs/8.jpg',
    'sample_imgs/9.jpg',
    'sample_imgs/10.jpg',
    'sample_imgs/11.jpg',
    'sample_imgs/12.jpg',
]

for url in images:
    print(url)
    print(get_colors(url))
    print('\n')
