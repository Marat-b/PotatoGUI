import pathlib

def create_dirs():
    pathlib.Path('db').mkdir(parents=True, exist_ok=True)
    pathlib.Path('videos').mkdir(parents=True, exist_ok=True)
    pathlib.Path('weights').mkdir(parents=True, exist_ok=True)