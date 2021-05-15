from __future__ import annotations
import os
import json
from codecs import open
from dataclasses import dataclass

EXT = ['.png', '.jpg', '.gif']
RED = '\033[1;31m'
RESET = '\033[0;0m'
path = os.path


@dataclass
class E:
    void: bool
    tag: str
    attr: dict
    text: list[str]
    children: list[E]

    def tolist(self):
        # start tag
        s = f'<{self.tag}'
        # add attributes
        for attr, value in self.attr.items():
            s += f' {attr}="{value}"'
        if self.void:
            return [s + '/>']
        elif not len(self.children) and len(self.text) < 2:
            # if no children and text is at most 1 line
            return [s + '>' + ''.join(self.text) + '</' + self.tag + '>']
        else:
            l = [s + '>']
            # text
            for t in self.text:
                l.append('\t' + t)

            # children
            for ch in self.children:
                l.append('\t' + ch.tolist())
            return l + [f'</{self.tag}>']
