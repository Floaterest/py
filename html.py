#!/usr/bin/env python

import os, sys
from codecs import open
from dataclasses import dataclass


@dataclass
class Html:
    title: list
    style: list
    body: list
    script: list


class Writer:
    def __init__(self, path):
        self.path = path
        self.files = [p for p in os.listdir() if self.is_image(p)]
        self.version = 0
        self.html = Html([os.path.basename(os.getcwd())], [], [], [])

    @staticmethod
    def is_image(path: str) -> bool:
        return any([path.endswith(ext) for ext in ['.png', '.jpg']])

    @staticmethod
    def get_id(filename: str) -> str:
        # assume that the last 8 chars are '-001.png' for example
        return filename[:-8]

    def add_styles(self, styles: dict):
        for selector, style in styles.items():
            self.html.style.append(selector + '{')
            self.html.style += [f'\t{k}: {v};' for k, v in style.items()]
            self.html.style.append('}')

    def write(self):
        with open(self.path, 'w+', 'utf8') as f:
            f.write(f'<!-- Version {self.version} -->\n')

            f.write('<html><head>\n')
            f.write('<meta content="text/html;charset=utf-8" http-equiv="Content-Type">\n')
            f.write('<meta content="utf-8" http-equiv="encoding">\n')

            for tag, content in self.html.__dict__.items():
                endl = '' if tag == 'title' else '\n'
                if content:
                    if tag == 'script':
                        s = f'<{tag} type="text/javascript">\n{endl.join(content)}\n</{tag}>\n'
                    else:
                        s = f'<{tag}>{endl}{endl.join(content)}{endl}</{tag}>\n'
                    f.write(s)

            f.write('<html>')

    def top_to_bottom(self):
        self.version = 20200905
        self.add_styles({
            'body': {
                'background': 'black',
                'margin': 0,
                'width': '200%'
            },
            'img': {
                'display': 'block',
                'margin': '0 auto'
            },
            'p': {
                'text-align': 'center',
                'color': 'white'
            }
        })

        self.html.body.append(f'<p>{self.html.title}</p>')
        for f in self.files:
            self.html.body.append(f'<img alt="{f}" src="{f}"/>')

    def tab(self):
        """
        Image file name should be {tab}-{index}{.png or .jpg}
        To seperate different chapters with the same id, you can use
        e.g. '123456-1-003.png'
        """
        self.version = 20201023
        self.add_styles({
            'body': {
                'background': 'black',
                'margin': 0,
                'width': '300%',
            },
            'img': {
                'display': 'block',
                'margin': '0 auto',
            },
            'p, span': {
                'text-align': 'center',
                'color': 'white',
                'font-size': '100px',
                'margin': 0
            },
            '#tab': {
                'position': 'fixed',
                'width': '100%',
                'bottom': 0,
                'left': 0,
                'white-space': 'nowrap',
                'overflow': 'auto',
            },
            'span': {
                'padding': '0 0.5em',
                'user-select': 'none',
            },
            '.selected': {
                'color': 'red'
            }
        })
        # js madness
        self.html.script = [
            "Array.from(document.getElementsByTagName('span')).forEach(s=>s.addEventListener('click',()=>{Array.from(document.getElementsByTagName('p')).forEach(p=>p.style.display=s.classList.contains('selected')||p.classList.contains(s.innerText)?'block':'none');Array.from(document.getElementsByTagName('span')).forEach(t=>t.classList.remove('selected'));s.classList.toggle('selected');window.scroll({top:0})}));"
        ]
        endl = '\n'
        gs = []
        for f in self.files:
            # 'g' because it's '/g/{id}'
            g = self.get_id(f)
            if g not in gs:
                gs.append(g)
                self.html.body.append(f'<p class="{g}">{g}</p>')
            self.html.body.append(f'<p class="{g}"><img alt="{f}" src="{f}"/></p>')
        self.html.body.append(f'<div id="tab">\n{endl.join([f"<span>{g}</span>" for g in gs])}\n</div>')


if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    os.chdir(sys.argv[1])

w = Writer('!Readme.html')
w.top_to_bottom()
w.write()
