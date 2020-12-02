import os, sys
from codecs import open
from dataclasses import dataclass

extensions = ['.png', '.jpg', '.gif']

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
        return any([path.endswith(ext) for ext in extensions])

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
        self.version = 20210127
        self.add_styles({
            'body': {
                'background': 'black',
                'margin': 0,
                'width': '200%',
                'color': 'white',
                'user-select': 'none'
            },
            'img': {
                'display': 'block',
                'margin': '0 auto',
            },
            '#select': {
                'font-size': '4em',
                'position': 'fixed',
                'line-height': 0.5,
                'top': '50%',
                'left': '50%',
                'z-index': 1,
            },
            '#content': {
                'text-align': 'center',
                'z-index': 0,
            }
        })
        # js madness
        self.html.script = [
            "document.body.scrollLeft=document.body.clientWidth/2;const content=document.getElementById('content'),select=document.getElementById('select');select.style.marginTop= -select.offsetHeight/2+'px';select.style.marginLeft= -select.offsetWidth/2+'px';select.style.display='none';Array.from(content.children).forEach(p=>p.addEventListener('click',()=>{if(content.style.filter==='none'||!content.style.filter){content.style.filter='brightness(10%)';select.style.display='inline'}else{content.style.filter=select.style.display='none'}}));Array.from(select.children).forEach(p=>p.addEventListener('click',()=>{if(p.style.filter==='none'||!p.style.filter){p.style.filter='brightness(30%)';document.getElementById(p.innerText).style.display='none'}else{p.style.filter='none';document.getElementById(p.innerText).style.display='block'}document.body.scrollTop=0}));"
        ]

        # select
        fs = {}
        self.html.body.append('<div id="select">')
        for f in self.files:
            i = self.get_id(f)
            if i not in fs:
                self.html.body.append(f'\t<p>{i}</p>')
                fs[i] = []
            fs[i].append(f)
        self.html.body.append('</div>')
        # images
        self.html.body.append('<div id="content">')
        # for each id
        for i, l in fs.items():
            self.html.body.append(f'\t<p id="{i}">')
            self.html.body.append(f'\t\t{i}')
            for f in l:
                self.html.body.append(f'\t\t<img alt="{f}" src="{f}"/>')
            self.html.body.append('\t</p>')
        self.html.body.append('</div>')


print(sys.argv)
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    os.chdir(sys.argv[1])

w = Writer('0.html')
w.top_to_bottom()
w.write()
