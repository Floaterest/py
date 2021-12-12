from __future__ import annotations
import os, sys
from codecs import open
from dataclasses import dataclass, field

path = os.path
EXTENSIONS = ['.png', '.jpg', '.gif']
SRC = path.abspath('html/')
VOID = ['meta', 'img', 'br']
NO_INDENT = ['html']
RED = '\033[1;31m'
RESET = '\033[0;0m'


@dataclass
class E:
    tag: str
    attr: dict = field(default_factory=dict)
    text: list[str] = field(default_factory=list)
    children: list[E] = field(default_factory=list)

    def str(self, indent=0) -> str:
        t = '\t' * indent
        # start tag
        s = t + '<' + self.tag
        # add attributes
        for attr, value in self.attr.items():
            s += f' {attr}="{value}"'
        if self.tag in VOID:
            return s + '>\n'
        elif not len(self.children) and len(self.text) < 2:
            # if no children and text is at most 1 line
            return s + '>' + ''.join(self.text) + '</' + self.tag + '>\n'
        else:
            tt = t + '\t'
            s += '>\n'
            # text
            for line in self.text:
                s += tt + line
            # children
            if self.tag not in NO_INDENT:
                indent += 1
            for ch in self.children:
                s += ch.str(indent)
            return s + t + '</' + self.tag + '>\n'

    def append(self, element: E):
        self.children.append(element)
        return self

    def append_to(self, element: E):
        element.children.append(self)
        return self


MODES = {
    't2b': [20200415, ['t2b.css'], []],
    'tab': [20210319, ['t2b.css', 'tab.css'], ['tab.js']],
}


def is_image(fn: str) -> bool:
    return any([fn.endswith(ext) for ext in EXTENSIONS])


def get_src(fn: str):
    with open(path.join(SRC, fn), 'r', 'utf8') as f:
        return f.readlines()


def init_html(title: str):
    html = E('html', attr={'lang': 'en'})
    return (
        html,
        E('head', children=[
            E('meta', attr={'charset': 'utf8'}),
            E('title', text=[title]),
        ]).append_to(html),
        E('body').append_to(html)
    )


class Writer:
    def __init__(self, mode: str, wrap: int):
        """
        do os.chdir() before init
        """
        self.html, self.head, self.body = init_html(path.basename(os.getcwd()))
        self.files = sorted([f for f in os.listdir() if is_image(f.lower())])
        self.wrap = wrap
        self.generate = self.__getattribute__(mode)
        self.version, styles, scripts = MODES[mode]
        # add styles and scripts
        for style in styles:
            self.head.append(E('style', text=get_src(style)))
        self.head.append(E('style', text=get_src('wrap.css' if wrap else 'wrap0.css')))
        for script in scripts:
            self.html.append(E('script', text=get_src(script)))

    def tab(self):
        def get_chapter(fn: str) -> str:
            return fn[:-8]

        # region body
        # region select
        select = E('div', attr={'id': 'select'}, children=[
            E('code', attr={'id': 'invert'}, text=['invert'])
        ]).append_to(self.body)

        fs = {}
        for f in self.files:
            chap = get_chapter(f)
            if chap not in fs:
                fs[chap] = []
                select.append(E('p', text=[chap]))
            fs[chap].append(f)
        # endregion select

        # region content
        content = E('div', attr={'id': 'content'}).append_to(self.body)
        # foreach chapter
        page = 1
        for chapter, files in fs.items():
            chap = E('p', attr={'id': chapter}, text=[chapter + '\n']).append_to(content)
            # foreach image
            for f in files:
                chap.append(E('img', attr={'alt': f, 'src': f}))
                if not (self.wrap and (self.wrap + page) % 2):
                    """
                    add <br> if
                        1. wrap == 0
                        2. wrap and page number(1-indexed) are both odd or even 
                    """
                    chap.append(E('br'))
                page = (page + 1) % 2
        # endregion content
        # endregion body

    def write(self, fn: str):
        self.generate()
        with open(fn + '.html', 'w', 'utf8') as f:
            f.write('<!doctype html>\n')
            f.write(f'<!-- Version {self.version} -->\n')
            f.write(self.html.str())


os.chdir(sys.argv[1])
w = Writer('tab', 1)
w.write('0')
