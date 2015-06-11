def make_torrent(file):
    import libtorrent as lt

    fs = lt.file_storage()
    piece_size = 256 * 1024
    lt.add_files(fs, file.path)

    t = lt.create_torrent(fs, piece_size)
    lt.set_piece_hashes(t, file.storage_folder)
    t.add_url_seed(file.blob)
    t.set_creator('a2p')

    torrent = t.generate()
    return lt.bencode(torrent)
