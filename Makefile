all: static/js/build.min.js static/css/build.css

static/js/build.min.js: static/js/build.js
	node_modules/uglify-js/bin/uglifyjs -o $@ $^

static/js/build.js: static/js/source.js
	node_modules/browserify/bin/cmd.js -o $@ $^

static/css/build.css: static/css/source.scss
	sass $^ $@
