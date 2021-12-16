from __future__ import annotations
import os, sys
from codecs import open
from dataclasses import dataclass, field

path = os.path
EXTENSIONS = ['.png', '.jpg', '.gif']
SRC = path.abspath('html/')
VOID = ['meta', 'img', 'br']
RED = '\033[1;31m'
RESET = '\033[0;0m'


@dataclass
class Element:
    tag: str
    attr: dict = field(default_factory=dict)
    text: list[str] = field(default_factory=list)
    children: list[Element] = field(default_factory=list)
    # whether appends '\n' at end of closed tag
    eol: bool = True
    # whether itself should be indented in the final html
    indent: bool = True

    def str(self, indent=0) -> str:
        # no indent if not self.indent
        indent *= self.indent
        t = '\t' * indent
        n = '\n' * self.eol
        # start tag
        s = t + '<' + self.tag
        # add attributes
        for attr, value in self.attr.items():
            s += f' {attr}="{value}"'
        if self.tag in VOID:
            return s + '>' + n
        elif not len(self.children) and len(self.text) < 2:
            # if no children and text is at most 1 line
            return s + '>' + ''.join(self.text) + '</' + self.tag + '>' + n
        else:
            tt = t + '\t'
            s += '>\n'
            # text
            for line in self.text:
                s += tt + line
            # children
            for ch in self.children:
                s += ch.str(indent + 1)
            return s + t + '</' + self.tag + '>' + n

    def append(self, element: Element):
        self.children.append(element)
        return self

    def append_to(self, element: Element):
        element.children.append(self)
        return self


MODES = {
    't2b': [['t2b.css'], []],
    'tab': [['t2b.css', 'tab.css'], ['tab.js']],
}


def is_image(fn: str) -> bool:
    return any([fn.endswith(ext) for ext in EXTENSIONS])


def get_src(fn: str):
    with open(path.join(SRC, fn), 'r', 'utf8') as f:
        return f.readlines()


def init_html(title: str):
    html = Element('html', attr={'lang': 'en'})
    return (
        html,
        Element('head', indent=False, children=[
            Element('meta', attr={'charset': 'utf8'}),
            Element('title', text=[title]),
        ]).append_to(html),
        Element('body', indent=False).append_to(html)
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
        styles, scripts = MODES[mode]
        # add styles and scripts
        for style in styles:
            self.head.append(Element('style', text=get_src(style)))
        self.head.append(Element('style', text=get_src('wrap.css' if wrap else 'wrap0.css')))
        for script in scripts:
            self.html.append(Element('script', indent=False, text=get_src(script)))

    def tab(self):
        def get_chapter(fn: str) -> str:
            return fn[:-8]

        # region body
        # region select
        select = Element('div', attr={'id': 'select'}, children=[
            Element('code', attr={'id': 'invert'}, text=['invert'])
        ]).append_to(self.body)

        fs = {}
        for f in self.files:
            chap = get_chapter(f)
            if chap not in fs:
                fs[chap] = []
                select.append(Element('p', text=[chap]))
            fs[chap].append(f)
        # endregion select

        # region content
        content = Element('div', attr={'id': 'content'}).append_to(self.body)
        # if wrap == 0, then shift = 0
        # elif wrap at page 2n (wrap == 2), then shift = 1
        # elif wrap at page 2n+1 (wrap == 1), then shift = -1
        shift = not self.wrap or 2 * self.wrap - 3
        page = 1
        for chapter, files in fs.items():
            chap = Element('p', attr={'id': chapter}, text=[chapter + '\n']).append_to(content)
            # upper bound of the list
            upper = len(files) - 1
            # foreach image
            for i in range(len(files)):
                # if wrap and page number(1-indexed) are both even or both odd
                both = not (self.wrap + page) % 2
                # always eol and indent if self.wrap == 0
                # and always eol at last element and indent at first element
                eol = not self.wrap or not both or i == upper
                indent = not self.wrap or both or not i
                # make sure i is in list's range
                i = max(min(i + shift, upper), 0)
                chap.append(Element('img', attr={
                    'alt': files[i], 'src': files[i]
                }, eol=eol, indent=indent))

                shift = -shift
                page += 1

        # endregion content
        # endregion body

    def write(self, fn: str):
        self.generate()
        with open(fn + '.html', 'w', 'utf8') as f:
            f.write('<!doctype html>\n')
            f.write(self.html.str())


os.chdir(sys.argv[1])
# note: wrapping is based on global page number
# not page number inside each chapter
w = Writer('tab', 1)
w.write('0')
