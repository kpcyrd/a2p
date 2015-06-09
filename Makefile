all: static/js/build.js static/css/build.css

static/js/build.js: static/js/source.js
	cat $^ > $@

static/css/build.css: static/css/source.scss
	sass $^ $@
