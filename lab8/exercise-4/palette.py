#!/usr/bin/env python3

import sys
import struct
from zlib import crc32
import os

# PNG file format signature
pngsig = b'\x89PNG\r\n\x1a\n'

def swap_palette(filename, n, run_type):
    # open in read+write mode
    with open(filename, 'r+b') as f:
        f.seek(0)
        # verify that we have a PNG file
        sig = f.read(len(pngsig))
        if sig != pngsig:
            raise RuntimeError('not a png file!')

        while True:
            chunkstr = f.read(8)
            if len(chunkstr) != 8:
                # end of file
                break

            # decode the chunk header
            length, chtype = struct.unpack('>L4s', chunkstr)
            # print("type: ", chtype)

            # we only care about palette chunks
            if chtype == b'PLTE':
                curpos = f.tell()
                paldata = f.read(length)
                if run_type == 1:
                    # replace palette entry n with white, the rest with black
                    paldata = (b"\x00\x00\x00" * n) + b"\xff\xff\xff" + (b"\x00\x00\x00" * (256 - n - 1))
                elif run_type == 2:
                    # replace palette entry 127 to 127 + n with white, the rest with black
                    paldata = (b"\x00\x00\x00" * 127) + (b"\xff\xff\xff"*n) + (b"\x00\x00\x00" * (256 - (127 + n)))
                else:
                    raise RuntimeError("No this run type!")

                # go back and write the modified palette in-place
                f.seek(curpos)
                f.write(paldata)
                f.write(struct.pack('>L', crc32(chtype+paldata)&0xffffffff))
            else:
                # skip over non-palette chunks
                f.seek(length+4, os.SEEK_CUR)

if __name__ == '__main__':
    import shutil
    try:
        os.mkdir('sample')
    except FileExistsError:
        print("File exists!")
    try:
        os.mkdir('sample2')
    except FileExistsError:
        print("File exists!")

    for idx in range(256):
        filename = f"sample/{idx}.png"
        shutil.copyfile('ctf-example.png', filename)
        swap_palette(filename, idx, 1)

    for idx in range(256):
        filename = f"sample2/{idx}.png"
        shutil.copyfile('ctf-example.png', filename)
        swap_palette(filename, idx, 2)
    
    