from codecs import open
from datetime import datetime, timedelta
import os, re, sys

sh = timedelta(seconds=int(sys.argv[2]))
os.chdir(sys.argv[1])
t = re.compile(r'(\d\d:){2}\d{2},\d{3}\s-->\s(\d\d:){2}\d{2},\d{3}')
for file in [f for f in os.listdir() if f.endswith('.srt')]:
    lines = []
    with open(file, 'r', 'utf8') as f:
        while line := f.readline():
            if t.match(line):
                start = datetime.strptime(line[:12], '%H:%M:%S,%f')
                end = datetime.strptime(line[17:29], '%H:%M:%S,%f')
                line = (start + sh).strftime('%H:%M:%S,%f')[:12]
                line += ' --> '
                line += (end + sh).strftime('%H:%M:%S,%f')[:12]
                line += '\n'
            lines.append(line)
    with open(file, 'w', 'utf8') as f:
        f.writelines(lines)
