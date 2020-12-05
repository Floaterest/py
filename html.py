import os
import sys
import json
from codecs import open
from dataclasses import dataclass
import xml.etree.cElementTree as ET
import xml.dom.minidom

# an image is defined as files with these extensions
EXTENSIONS = ['.png', '.jpg', '.gif']


@dataclass
class Mode:
    style: dict
    script: str


@dataclass
class Config:
    # destination filename
    dest: str
    # display mode
    mode: str
    # css and js of each mode
    modes: dict


CONFIG = 'config.json'
with open(CONFIG, 'r') as f:
    config = Config(**json.load(f)[os.path.basename(__file__)])
    modes = config.modes


def is_image(fn: str) -> bool:
    return any([fn.endswith(ext) for ext in EXTENSIONS])


def create_style(css: dict):
    return '\n'.join([
        selector + '{\n' + '\n'.join([
            f'\t{k}: {v};' for k, v in style.items()
        ]) + '\n}' for selector, style in css.items()
    ])


class Writer:
    def __init__(self, dest: str, mode: str):
        assert mode in modes, f"'{mode}' is not a valid mode!"

        self.dest = dest
        self.mode = mode
        self.files = [f for f in os.listdir() if is_image(f)]
        # region html
        self.html = ET.Element('html')
        # region head
        head = ET.SubElement(self.html, 'head')
        ET.SubElement(head, 'meta', {
            'content': 'text/html;charset=utf-8',
            'http-equiv': 'Content-Type',
        })
        ET.SubElement(head, 'title').text = os.path.basename(os.getcwd())

        ET.SubElement(head, 'style').text = create_style(modes[mode]['style'])
        # endregion head
        # endregion html

    def tab(self):
        def get_chapter(fn: str) -> str:
            return fn[:-8]

        # region body
        body = ET.SubElement(self.html, 'body')

        # region select
        select = ET.SubElement(body, 'div', id='select')

        fs = {}
        for f in self.files:
            chap = get_chapter(f)
            if chap not in fs:
                fs[chap] = []
                ET.SubElement(select, 'p').text = chap
            fs[chap].append(f)

        # endregion select

        # region content
        content = ET.SubElement(body, 'div', id='content')
        # foreach chapter
        for chapter, imgs in fs.items():
            chap = ET.SubElement(content, 'p', id=chapter)
            chap.text = chapter
            # foreach image
            for i in imgs:
                ET.SubElement(chap, 'img', {'alt': i, 'src': i})

        # endregion content
        # endregion body
        # add javascript
        ET.SubElement(self.html, 'script', type='text/javascript').text = modes['tab']['script']

    def write(self):
        exec(f'self.{self.mode}()')

        ET.ElementTree(self.html).write(self.dest, 'utf8')
        with open(self.dest, 'w', 'utf8') as f:
            f.write(xml.dom.minidom.parseString(ET.tostring(self.html)).toprettyxml())


if len(sys.argv) > 1:
    assert os.path.exists(sys.argv[1]), f"'{sys.argv[1]}' is not a valid directory!"
    os.chdir(sys.argv[1])

Writer(config.dest, config.mode).write()
