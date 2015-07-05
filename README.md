# a2p

Content addressable one click hoster. Features true progressive enhancement javascript and scriptability (see `bin/a2p2`).

## // TODO:

- [X] basic upload
- [x] fancy html5 file upload
- [ ] webrtc seeding swarm
- [X] auto torrent
- [ ] scp interface
- [ ] invent

## a2p2

```sh
bin/a2p2 http://127.0.0.1:5000 file1 file2 # uploads file1 and file2 to http://127.0.0.1:5000/
all_proxy=socks4a://127.0.0.1:9050 bin/a2p2 http://127.0.0.1:5000 file1 file2 # uploads with proxy
sudo install bin/a2p2 /usr/bin/a2p2 # install for all users as `a2p2`
alias a2p2x='all_proxy=socks4a://127.0.0.1:9050 a2p2 http://localhost:5000' # add shorthand `a2p2x file1 file2`
```

## License

a2p is free software in the terms of the GPLv3 licence.
