import constants as co
import emotes as e
import conf as c

from copy import deepcopy
from glob import iglob
import time
import os

class notetaker:
    files = []
    root = ''
    latest_changes = []
    context = None

    def __init__(self, user, username):
        self.uid = user
        self.uname = username
        self.root = '{}{}/'.format(c.root, user)
        if not os.path.exists(self.root):
            os.mkdir(self.root)
        self.files = [f.split(sep='/')[-1] for f in iglob(self.root + '*')]

    def ls(self):
        acc = '```File Name                 Line Count\n'
        for f in self.files:
            line_count = str(sum([1 for line in open(self.root+f, 'r')]))
            acc += f + '\t'*6 + line_count + '\n'
        return acc + '```'

    def open_context(self, fname):
        fname = fname.replace('/', '').replace('..', '')
        self.context = self.root + fname
        if not fname in self.files:
            self.files.append(fname)
            self.write_to_context(co.IDENT)
        self.context = self.root + fname
        return e.GOOD[:-3]

    def close_context(self):
        self.context = None
        return e.GOOD[:-3]

    def write_to_context(self, type, data=''):
        if self.context is None:
            return '{}There is currenly no open file, use the `open` command'.format(e.CANNOT)
        with open(self.context, 'a') as f:
            if type == co.IDENT:
                ctime = round(time.time())
                w = co.HEADER.format(
                    self.context.split(sep='/')[-1],
                    self.uname,
                    time.strftime('%d-%m-%Y', time.gmtime(ctime)),
                    ctime)
            elif type == co.TOPIC:
                w = '### {}\n'.format(data)
            elif type == co.TXT:
                w = '{}\n'.format(data)
            f.write(w)
            self.latest_changes.append({deepcopy(self.context) : w})
            return 0

    def read_context(self):
        if self.context is None:
            return '{}There is currenly no open file, use the `open` command'.format(e.CANNOT)
        with open(self.context, 'r') as f:
            data = f.read()
        if len(data) >= 2000:
            return '{}File too big to show'.format(e.ERROR)
        return '```{}```'.format(data)

    def delete(self, filename):
        if not filename in self.files:
            return '{}Nonexistent file'.format(e.ERROR)
        os.remove(self.root + filename)
        return e.GOOD[:-3]

    def undo(self):
        if len(self.latest_changes) > 0:
            latest_change = self.latest_changes.pop()
            key = list(latest_change.keys())[0]
            with open(key, 'r') as f:
                tmp = f.read()
            with open(key, 'w') as f:
                f.write(tmp.replace(latest_change[key], ''))
            return '{}Undo process was successful. Changed: {}'.format(e.GOOD, key.split(sep='/')[-1])
        return '{}There are no more changes that can be undone'.format(e.INFO)
