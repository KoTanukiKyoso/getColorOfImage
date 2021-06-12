import cv2
import numpy as np
from skimage import io
from skimage import color
import tkinter as tk
from tkinter import filedialog

colors = {
    "red": {
        "name": "red", "ja": u"赤",
        "r": 255, "g": 0, "b": 0,
    },
    "yellow": {
        "name": "yellow", "ja": u"黄",
        "r": 255, "g": 255, "b": 0,
    },
    "orange": {
        "name": "orange", "ja": u"橙",
        "r": 255, "g": 165, "b": 0,
    },
    "blue": {
        "name": "blue", "ja": u"青",
        "r": 0, "g": 0, "b": 255,
    },
    "green": {
        "name": "green", "ja": u"緑",
        "r": 0, "g": 128, "b": 0,
    },
    "indigoBlue": {
        "name": "indigoBlue", "ja": u"藍",
        "r": 4, "g": 60, "b": 120,
    },
    "purple": {
        "name": "purple", "ja": u"紫",
        "r": 128, "g": 0, "b": 128,
    },
    # 水色　等検証
    "black": {
        "name": "black", "ja": u"黒",
        "r": 0, "g": 0, "b": 0,
    },
    "white": {
        "name": "white", "ja": u"白",
        "r": 255, "g": 255, "b": 255,
    },
    "grey": {
        "name": "grey", "ja": u"灰",
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


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.selectDir = tk.Button(self, text=u"画像ファイル（jpg,png）を選択", command=self.selectDirectory)
        self.selectDir.pack(side="top")

        self.dirPath = tk.StringVar()
        self.dirPath.set(u"選択画像：")
        self.Static1 = tk.Label(self, textvariable=self.dirPath)
        self.Static1.pack()

        self.colors = tk.StringVar()
        self.colors.set(u"含まれる色要素：")
        self.Static2 = tk.Label(self, textvariable=self.colors)
        self.Static2.pack()

    def selectDirectory(self):
        fld = filedialog.askopenfilename()
        self.dirPath.set(u"選択画像：" + fld)
        self.colors.set(u"含まれる色要素：" + get_colors(fld))


root = tk.Tk()
app = Application(master=root)
root.title(u"サハスラ")
root.geometry("400x300")

app.mainloop()
