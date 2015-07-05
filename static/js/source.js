'use strict';

window.onload = function()  {
    var form = document.forms[0];
    if(form) {
        var dest = form.action;

        var submit = document.getElementById('submit');
        var progressBar = document.getElementById('progress');
        var file = form.file;

        var wrapcb = function(cb, calls) {
            cb = cb || {};
            calls.forEach(function(x) {
                cb[x] = cb[x] || function(){};
            });
            return cb;
        };

        var streamFile = function(file, cb) {
            cb = wrapcb(cb, ['chunk', 'done']);

            var chunkSize = 16384;
            var sliceFile = function(offset) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    cb.chunk(e.target.result);

                    if (file.size > offset + e.target.result.byteLength) {
                        setTimeout(sliceFile, 0, offset + chunkSize);
                    } else {
                        cb.done();
                    }
                };
                var slice = file.slice(offset, offset + chunkSize);
                reader.readAsArrayBuffer(slice);
            };

            sliceFile(0);
        };

        var hashFile = function(file, cb) {
            var sha1 = require('crypto').createHash('sha1');

            streamFile(file, {
                chunk: function(chunk) {
                    sha1.update(new Uint8Array(chunk));
                },

                done: function() {
                    cb(sha1.digest('hex'));
                }
            });
        };

        var hasFile = function(file, cb) {
            cb = wrapcb(cb, ['known', 'unknown']);

            hashFile(file, function(hash) {
                var xhr = new XMLHttpRequest();
                var url = '/has/' + hash + '?n=' + file.name;
                xhr.open('GET', url, true);
                xhr.addEventListener('load', function() {
                    if(xhr.status == 200) {
                        cb.known(xhr.responseURL);
                    } else {
                        cb.unknown();
                    }
                }, false);
                xhr.send();
            });
        };

        var sendFile = function(file, cb) {
            cb = wrapcb(cb, ['progress', 'done', 'error']);

            var xhr = new XMLHttpRequest();
            var fd = new FormData();

            xhr.open('POST', dest, true);
            xhr.upload.addEventListener('progress', cb.progress, false);
            xhr.addEventListener('load', cb.done, false);
            xhr.addEventListener('error', cb.error, false);
            fd.append('file', file);
            xhr.send(fd);
        };

        file.disabled = false;
        submit.disabled = false;

        form.onsubmit = function(e) {
            e.preventDefault();

            var file = form.file;
            if(file.files.length == 1) {
                file.disabled = true;
                submit.disabled = true;
                progressBar.hidden = false;

                hasFile(file.files[0], {
                    known: function(url) {
                        window.location = url;
                    },

                    unknown: function() {
                        sendFile(file.files[0], {
                            error: function(error) {
                                alert('upload failed');
                                window.location.reload();
                            },
                            progress: function(progress) {
                                progressBar.value = progress.loaded;
                                progressBar.max = progress.total;
                            },
                            done: function(xhr) {
                                window.location = xhr.target.responseURL;
                            }
                        });
                    }
                });
            }
        };
    }
};
