import cv2
import os
import io
import numpy as np
import copy
import csv
import requests
import re
from PIL import Image


def delete_empty_images(dir):
    empty = cv2.imread("empty_image.jpg")
    h, w, d = empty.shape
    num_files = len([1 for x in list(os.scandir(dir)) if x.is_file()])

    counter = 0
    i = 0

    while counter < num_files:
        img = cv2.imread(dir + str(i) + ".jpg")
        if img is not None:
            counter += 1
            img = cv2.resize(img, (w, h))
            diff = cv2.subtract(empty, img)
            result = not np.any(diff)

            if result is True:
                print(i)
                os.remove(dir + str(i) + ".jpg")

        i += 1


def download_and_save_imagenet():
    with open("shoes.txt") as file:
        content = file.readlines()
    content = [x.strip() for x in content]

    for i in range(0, len(content)):
        url = content[i]

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200 and response.content.find(b'head') == -1 and len(response.content) > 3:
                print(i)

                try:
                    f = io.BytesIO(response.content)
                    img = Image.open(f)

                    pil_image = img.convert("RGB")
                    cv_image = np.array(pil_image)
                    img = cv_image[:, :, ::-1].copy()

                    filename = "zdjecia/" + str(i) + ".jpg"
                    cv2.imwrite(filename, img)
                except OSError:
                    print("Blad ladowania zdjecia")

        except requests.exceptions.ConnectionError:
            print("Blad nawiazywania polaczenia")
        except requests.exceptions.ReadTimeout:
            print("Zbyt dlugi czas oczekiwania")
        except requests.exceptions.TooManyRedirects:
            print("Zbyt wiele przekierowan")
        except requests.exceptions.MissingSchema:
            print("Brak Schema")
        except requests.exceptions.InvalidSchema:
            print("Brak adaptorow polaczenia")


download_and_save_imagenet()
delete_empty_images("zdjecia")
