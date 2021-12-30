from __future__ import annotations
from os import path, getcwd
from codecs import open
from dataclasses import dataclass, field

SRC = path.abspath('utils/')
VOID = ['meta', 'img', 'br']
MODES = {
    # 't2b': [['t2b.css'], []],
    'tab': [['t2b.css', 'tab.css'], ['tab.js']],
}


@dataclass
class Element:
    tag: str
    attr: dict = field(default_factory=dict)
    text: list[str] = field(default_factory=list)
    children: list[Element] = field(default_factory=list)
    # whether itself should be indented in the final utils
    indent: bool = True

    def str(self, indent=0) -> str:
        # no indent if not self.indent
        indent *= self.indent
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
            if self.children and self.text:
                s += '\n'
            # children
            for ch in self.children:
                s += ch.str(indent + 1)
            return s + t + '</' + self.tag + '>\n'

    def append(self, element: Element):
        self.children.append(element)
        return self

    def append_to(self, element: Element):
        element.children.append(self)
        return self


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
    def __init__(self, mode: str, wrap: int, files: list[str]):
        """
        do os.chdir() before init
        """
        self.html, self.head, self.body = init_html(path.basename(getcwd()))
        self.files = files
        self.wrap = wrap
        self.generate = self.__getattribute__(mode)
        styles, scripts = MODES[mode]
        # add styles and scripts
        for style in styles:
            self.head.append(Element('style', text=get_src(style)))
        self.head.append(Element('style', text=get_src('wrap.css' if wrap else 'wrap0.css')))
        for script in scripts:
            self.html.append(Element('script', indent=False, text=get_src(script)))

    def __table(self, chapter: str, files: list[str], i: int = 1) -> [int, Element]:
        tr = Element('tr')
        table = Element('table', attr={'id': chapter, 'class': 'chapter'})
        tbody = Element('tbody').append_to(table)
        for f in files:
            # add img to td to tr
            tr.append(Element('td').append(Element('img', attr={'alt': f, 'src': f})))
            # create new tr when going to wrap
            if not (self.wrap + i) % 2:
                tbody.append(tr)
                tr = Element('tr')
            i = (i + 1) % 2
        tbody.append(tr)
        return i, table

    @staticmethod
    def __div(chapter: str, files: list[str]) -> Element:
        return Element('div', attr={
            'id': chapter,
            'class': 'chapter'
        }, text=[chapter], children=[
            Element('img', attr={'alt': f, 'src': f}) for f in files
        ])

    def tab(self):
        def get_chapter(fn: str) -> str:
            return fn[:-8]

        # region body
        # region select
        select = Element('div', attr={'id': 'select'}, children=[
            Element('code', attr={'id': 'invert'}, text=['invert'])
        ]).append_to(self.body)

        chapters = {}
        for f in self.files:
            chap = get_chapter(f)
            if chap not in chapters:
                chapters[chap] = []
                select.append(Element('p', text=[chap]))
            chapters[chap].append(f)
        # endregion select

        # region divs or tables
        if self.wrap:
            page = 1
            for chap, files in chapters.items():
                page, table = self.__table(chap, files, page)
                self.body.append(table)
        else:
            for chap, files in chapters.items():
                self.body.append(self.__div(chap, files))
        # endregion divs or tables
        # endregion body
        return self.html

    def write(self, fn: str):
        html = self.generate()
        with open(fn + '.html', 'w', 'utf8') as f:
            f.write('<!doctype html>\n')
            f.write(html.str())
