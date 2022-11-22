import os
import pathlib

from config.config import DEEPSORT, DETECTRON2


def create_dirs():
    pathlib.Path('db').mkdir(parents=True, exist_ok=True)
    pathlib.Path('videos').mkdir(parents=True, exist_ok=True)
    pathlib.Path('weights').mkdir(parents=True, exist_ok=True)

    if not os.path.exists(DEEPSORT):
        print(f'Не найден файл {DEEPSORT}')
        exit(1)

    if not os.path.exists(DETECTRON2):
        print(f'Не найден файл {DETECTRON2}')
        exit(1)