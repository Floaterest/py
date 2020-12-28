import os
import sys


def is_image(filename: str) -> bool:
    for ext in ['.jpg', '.png', '.gif']:
        if filename.endswith(ext):
            return True
    else:
        return False


os.chdir(sys.argv[1])

images = sorted([f for f in os.listdir() if is_image(f)])

cps = sys.argv[2:]
l = len(cps)
cur = 0
for i in images:
    if cur < l and i[:-4].endswith(cps[cur]):
        cur += 1
    os.rename(i, f'{i[:i.index("-")]}-{cur:02d}-{i[-7:]}')
