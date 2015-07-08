all: static/js/build.min.js static/css/build.css

static/js/build.min.js: static/js/build.js
	node_modules/minify/bin/minify.js $^ > $@

static/js/build.js: static/js/source.js
	node_modules/browserify/bin/cmd.js -o $@ $^ -i base64-js -i ieee754 -i is-array -i util

static/css/build.css: static/css/source.scss
	node_modules/node-sass/bin/node-sass --output-style compressed $^ > $@

.PHONY: clean
clean:
	rm -- static/*/build.*
