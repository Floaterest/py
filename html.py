import os, json, argparse
from typing import List
from codecs import open
from dataclasses import dataclass
import xml.etree.cElementTree as ET
from xml.dom.minidom import parseString
from xml.sax.saxutils import unescape

# an image is defined as files with these extensions
EXTENSIONS = ['.png', '.jpg', '.gif']


@dataclass
class Mode:
    name: str
    styles: List[str]
    scripts: List[str]
    version: int


@dataclass
class Config:
    # destination filename
    dest: str
    # display mode
    mode: str
    # css and js of each mode
    modes: dict


def is_image(fn: str) -> bool:
    return any([fn.endswith(ext) for ext in EXTENSIONS])


def read_all_text(fn: str) -> str:
    with open(fn, 'r', 'utf8') as f:
        return '\n' + f.read()


class Writer:
    def __init__(self, dest: str, mode: str):
        assert mode in config.modes, f"'{mode}' is not a valid mode!"

        folder = os.path.dirname(dest)
        self.dest = dest
        self.mode = Mode(name=mode, **config.modes[mode])
        self.files = [f for f in os.listdir(os.path.dirname(dest)) if is_image(f.lower())]

        assert self.files, folder + ' does not contain any images!'

        # region html
        self.html = ET.Element('html')
        # region head
        head = ET.SubElement(self.html, 'head')
        ET.SubElement(head, 'meta', {
            'content': 'text/html;charset=utf-8',
            'http-equiv': 'Content-Type',
        })
        ET.SubElement(head, 'title').text = os.path.basename(os.path.dirname(dest))

        # add styles
        for s in self.mode.styles:
            # looks ugly in the html file, but too lazy to fix it
            ET.SubElement(head, 'style').text = read_all_text(s)
        # endregion head
        self.body = ET.SubElement(self.html, 'body')
        # endregion html

    def t2b(self):
        """
        top to bottom
        """
        # region body
        for f in self.files:
            ET.SubElement(self.body, 'img', {'alt': f, 'src': f})
        # endregion body

    def t2b2(self):
        """
        top to bottom but odd pages are at left and even pages are at right
        (like a normal manga)
        """
        # same thing as t2b but image display is inline instead of block
        # and add <br> after each 2 images

        # region body

        for i, f in enumerate(self.files):
            ET.SubElement(self.body, 'img', {'alt': f, 'src': f})
            if not i % 2:
                ET.SubElement(self.body, 'br')
        # endregion body

    def tab(self):
        """
        tabs that can show/hide each chapter
        """

        def get_chapter(fn: str) -> str:
            return fn[:-8]

        # region body
        # region select
        select = ET.SubElement(self.body, 'div', id='select')
        ET.SubElement(select, 'code', id='inverse').text = 'inverse'

        fs = {}
        for f in self.files:
            chap = get_chapter(f)
            if chap not in fs:
                fs[chap] = []
                ET.SubElement(select, 'p').text = chap
            fs[chap].append(f)

        # endregion select

        # region content
        content = ET.SubElement(self.body, 'div', id='content')
        # foreach chapter
        for chapter, imgs in fs.items():
            chap = ET.SubElement(content, 'p', id=chapter)
            chap.text = chapter
            # foreach image
            for i in imgs:
                ET.SubElement(chap, 'img', {'alt': i, 'src': i})

        # endregion content
        # endregion body

    def write(self):
        exec(f'self.{self.mode.name}()')
        # add script
        for s in self.mode.scripts:
            ET.SubElement(self.html, 'script', type='application/javascript') \
                .text = read_all_text(s)

        s = ET.tostring(self.html)
        with open(self.dest + '.html', 'w', 'utf8') as f:
            f.write(f'<!-- Version {self.mode.version} -->\n')
            s = parseString(s).toprettyxml()
            # in <script> minidom thinks '>' should be converted to '&gt;'
            f.write(unescape(s))


CONFIG = 'config.json'
config = Config(**json.loads(read_all_text(CONFIG))[os.path.basename(__file__)])

parser = argparse.ArgumentParser(description='generate a gallary viewer with html')
parser.add_argument('path', type=str, nargs='?', default=os.getcwd(),
                    help='directory path (quoted with double quote)')
parser.add_argument('-m', '--mode', type=str, default=config.mode,
                    help=f'display mode, see {CONFIG} for all available modes')
args = parser.parse_args()

for r, ds, _ in os.walk(args.path):
    for d in ds:
        d = os.path.join(r,d)
        print(d, args.mode)
        f = os.path.join(d,config.dest)
        Writer(f, args.mode).write()
