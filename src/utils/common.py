EXTENSIONS = ['.png', '.jpg', '.gif']


def is_image(fn: str) -> bool:
    for ext in EXTENSIONS:
        if fn.endswith(ext):
            return True
    return False
