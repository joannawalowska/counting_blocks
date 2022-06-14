import argparse
import json
from pathlib import Path

import cv2

from processing.utils import perform_processing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('images_dir', type=str)
    parser.add_argument('results_file', type=str)
    args = parser.parse_args()

    images_dir = Path(args.images_dir)
    results_file = Path(args.results_file)

    images_paths = sorted([image_path for image_path in images_dir.iterdir() if image_path.name.endswith('.jpg')])
    results = {}

    wzor1 = cv2.imread('klocki/klocek_01.jpg')
    wzor2 = cv2.imread('klocki/klocek_02.jpg')
    wzor3 = cv2.imread('klocki/klocek_05.jpg')
    wzor4 = cv2.imread('klocki/klocek_04.jpg')
    wzor5 = cv2.imread('klocki/klocek_03.jpg')
    lista = [wzor1, wzor2, wzor3, wzor4, wzor5]

    for image_path in images_paths:
        image = cv2.imread(str(image_path))
        if image is None:
            print(f'Error loading image {image_path}')
            continue

        results[image_path.name] = perform_processing(image, lista)

    with results_file.open('w') as output_file:
        json.dump(results, output_file, indent=4)


if __name__ == '__main__':
    main()
