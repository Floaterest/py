EXTENSIONS = ['.png', '.jpg', '.gif']


def is_image(fn: str) -> bool:
    return any([fn.endswith(ext) for ext in EXTENSIONS])
