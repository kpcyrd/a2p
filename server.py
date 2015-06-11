#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, abort
from uuid import uuid4
import hashlib
import shutil
import os
import re

app = Flask(__name__)
app.config.from_object('config')


def find(name):
    hash = name.split('.')[0]
    print(hash)

    if not re.match('^[a-f0-9]{40}$', hash):
        return

    path = os.path.join(app.config['STORAGE_FOLDER'], hash)
    print(path)
    if not os.path.exists(path):
        return

    return path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/q/<name>')
def show(name):
    path = find(name)

    if not path:
        abort(404)

    return render_template('show.html', name=name, config=app.config)


@app.route('/q/<name>.torrent')
def torrent(name):
    path = find(name)

    if not path:
        abort(404)

    import libtorrent as lt

    fs = lt.file_storage()
    piece_size = 256 * 1024
    lt.add_files(fs, path)

    t = lt.create_torrent(fs, piece_size)
    lt.set_piece_hashes(t, app.config['STORAGE_FOLDER'])
    t.add_url_seed(app.config['BASE'] + '/static/storage/' + os.path.basename(path))
    t.set_creator('a2p')

    torrent = lt.bencode(t.generate())
    headers = {
        'Content-Type': 'application/x-bittorrent',
    }
    return torrent, 200, headers


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

    return redirect('/q/%s' % name)


if __name__ == '__main__':
    app.run(debug=True)
