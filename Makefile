all: static/js/build.js static/css/build.css

static/js/build.js: static/js/source.js
	node_modules/browserify/bin/cmd.js -o $@ $^

static/css/build.css: static/css/source.scss
	sass $^ $@
