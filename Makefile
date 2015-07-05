all: static/js/build.min.js static/css/build.css

static/js/build.min.js: static/js/build.js
	node_modules/minify/bin/minify.js $^ > $@

static/js/build.js: static/js/source.js
	node_modules/browserify/bin/cmd.js -o $@ $^ -i public-encrypt -i browserify-sign -i browserify-aes -i create-ecdh -i diffie-hellman -i pbkdf2 -i browserify-sign/algos -i ripemd160 -i readable-stream/duplex.js -i readable-stream/passthrough.js -i readable-stream/readable.js -i readable-stream/writable.js -i core-util-is -i base64-js -i ieee754 -i is-array -i _process -i randombytes -i isarray -i string_decoder/ -i create-hmac

static/css/build.css: static/css/source.scss
	sass $^ $@
