#!/usr/bin/env python
from flask import Flask, render_template, request, redirect
from uuid import uuid4
import hashlib
import shutil
import os

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/q/<name>')
def show(name):
    return render_template('show.html', name=name)


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
