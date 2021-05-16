from __future__ import annotations
import os
import json
from codecs import open
from dataclasses import dataclass, field

EXT = ['.png', '.jpg', '.gif']
VOID = ['meta', 'img']
NO_INDENT = ['head', 'body']
RED = '\033[1;31m'
RESET = '\033[0;0m'
path = os.path


@dataclass
class E:
    tag: str
    attr: dict = field(default_factory=dict)
    text: str = field(default_factory=str)
    children: list[E] = field(default_factory=list)

    def str(self) -> str:
        # start tag
        s = '<' + self.tag
        # add attributes
        for attr, value in self.attr.items():
            s += f' {attr}="{value}"'
        if self.tag in VOID:
            return s + '>\n'
        elif not len(self.children) and '\n' not in self.text:
            # if no children and text is at most 1 line
            return s + '>' + self.text + '</' + self.tag + '>\n'
        else:
            s += '>\n'
            if self.text:
                s += '\t' + self.text + '\n'
            # children
            for ch in self.children:
                if ch.tag not in NO_INDENT:
                    s += '\t'
                s += ch.str()
            return s + '</' + self.tag + '>\n'

    def find(self, tag: str):
        for ch in self.children:
            if ch.tag == tag:
                return ch
        return None


e = E('html', attr={'lang': 'en'}, children=[
    E('head', children=[
        E('meta', attr={'charset': 'utf8'}),
        E('title', text='py'),
    ]),
    E('body'),
])

with open('t.html', 'w', 'utf8') as f:
    f.write('<!doctype html>\n')
    f.write(e.str())
