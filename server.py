#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, abort
from urllib import urlencode
from urlparse import urljoin
from uuid import uuid4
import hashlib
import shutil
import utils
import os
import re

app = Flask(__name__)
app.config.from_object('config')


def find(name, real_name=None):
    hash = name.split('.')[0]

    if not re.match('^[a-f0-9]{40}$', hash):
        return

    path = os.path.join(app.config['STORAGE_FOLDER'], hash)
    if not os.path.exists(path):
        return

    return File(name, path, real_name)


class File(object):
    def __init__(self, name, path, real_name=None, config=app.config):
        self.config = config

        self.path = path
        self.name = name
        self.real_name = real_name
        self.sha1 = self.name.split('.')[0]
        self.storage_folder = self.config['STORAGE_FOLDER']

        self.direct = self.named_storage(self.name)
        self.show = self.named_link('q', self.name)
        self.torrent = self.named_link('q', self.name + '.torrent')
        self.blob = self.storage(self.sha1)

    def named_storage(self, name, **kwargs):
        return self.storage(name, n=self.real_name, **kwargs)

    def storage(self, name, **kwargs):
        return self.link(self.config['STORAGE_LINK'], name, **kwargs)

    def named_link(self, *path, **kwargs):
        return self.link(*path, n=self.real_name, **kwargs)

    def link(self, *path, **kwargs):
        url = self.config['BASE'] + '/'.join([''] + list(path))
        if kwargs:
            url += '?' + urlencode(kwargs)
        return url

    def make_torrent(self):
        return utils.make_torrent(self)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/q/<name>')
def show(name):
    real_name = request.args.get('n')
    file = find(name, real_name)

    if not file:
        abort(404)

    headers = {
        'X-Direct': file.direct,
        'X-Torrent': file.torrent,
    }
    return render_template('show.html', file=file), 200, headers


@app.route('/q/<name>.torrent')
def torrent(name):
    real_name = request.args.get('n')
    file = find(name, real_name)

    if not file:
        abort(404)

    headers = {
        'Content-Type': 'application/x-bittorrent',
    }

    return file.make_torrent(), 200, headers


@app.route('/has/<name>')
def has(name):
    real_name = request.args.get('n')
    file = find(name, real_name)

    if not file:
        abort(404)

    return file.show, 302, {'Location': file.show}


@app.route('/send', methods=['POST'])
def send():
    file = request.files['file']
    tmp = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid4()))

    h = hashlib.sha1()
    with open(tmp, 'wb') as f:
        while True:
            block = file.stream.read(app.config['CHUNKS'])
            if not block:
                break
            h.update(block)
            f.write(block)
    name = h.hexdigest()
    dest = os.path.join(app.config['STORAGE_FOLDER'], name)
    try:
        shutil.move(tmp, dest)
    except OSError:
        os.unlink(tmp)

    for ext in app.config['EXTENSIONS']:
        if file.filename.endswith(ext):
            dest_ext = '%s.%s' % (dest, ext)
            try:
                os.symlink(name, dest_ext)
            except OSError:
                pass
            name += '.' + ext
            break

    return redirect('/q/%s?%s' % (name, urlencode({'n': file.filename})))


if __name__ == '__main__':
    app.run(debug=True)
