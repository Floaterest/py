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
    name: str
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


def is_image(fn: str) -> bool:
    return any([fn.endswith(ext) for ext in EXTENSIONS])


def write_all_text(fn: str, s: str):
    with open(fn, 'w', 'utf8') as f:
        f.write(s)


def css_to_str(css: dict):
    return '\n'.join([
        selector + '{\n' + '\n'.join([
            f'\t{k}: {v};' for k, v in style.items()
        ]) + '\n}' for selector, style in css.items()
    ])


class Writer:
    def __init__(self, dest: str, mode: str):
        assert mode in config.modes, f"'{mode}' is not a valid mode!"

        self.dest = dest
        self.mode = Mode(name=mode, **config.modes[mode])
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

        # add style
        write_all_text(href := f'./{self.dest}.css', css_to_str(self.mode.style))
        ET.SubElement(head, 'link',
                      rel='stylesheet',
                      type='text/css',
                      href=href)
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
        write_all_text(src := f'./{self.dest}.js', self.mode.script)
        ET.SubElement(self.html, 'script',
                      type='application/javascript',
                      src=src).text = ' '

    def write(self):
        exec(f'self.{self.mode.name}()')
        s = ET.tostring(self.html)
        with open(self.dest + '.html', 'w', 'utf8') as f:
            f.write(xml.dom.minidom.parseString(s).toprettyxml())


if len(sys.argv) > 1:
    assert os.path.exists(sys.argv[1]), f"'{sys.argv[1]}' is not a valid directory!"
    os.chdir(sys.argv[1])

Writer(config.dest, config.mode).write()
