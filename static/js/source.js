'use strict';

window.onload = function()  {
    var form = document.forms[0];
    if(form) {
        var dest = form.action;

        var submit = document.getElementById('submit');
        var progressBar = document.getElementById('progress');
        var file = form.file;

        var sendFile = function(file, cb) {
            cb = cb || {};
            ['progress', 'done', 'error'].forEach(function(x) {
                cb[x] = cb[x] || function(){};
            });

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

                // TODO: check if file is already uploaded

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
        };
    }
};
