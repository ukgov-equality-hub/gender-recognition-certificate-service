import sys
from os import stat, remove
from pathlib import Path
import pyAesCrypt


def parse_cmd(argv, switch, val=None):
    for idx, x in enumerate(argv):
        if x in switch:
            if val:
                if len(argv) > (idx + 1):            
                    if not argv[idx + 1].startswith('-'):
                        return argv[idx + 1]
            else:
                return True


def main():
    filein = parse_cmd(sys.argv[1:], ['-i', '--filein', '--infile'], True)
    fileout = parse_cmd(sys.argv[1:], ['-o', '--fileout', '--outfile'], True)
    password = parse_cmd(sys.argv[1:], ['-p', '--password'], True)

    if filein is None:
        print("filein not specified")
        return
    elif not Path(filein).is_file():
        print("filein not found")
        return
    elif fileout is None:
        print("fileout not specified")
        return
    elif password is None:
        print("password not specified")
        return


    buffer_size = 64 * 1024
    enc_file_size = stat(filein).st_size

    with open(filein, 'rb') as fin:
        try:
            with open(fileout, 'wb') as fout:
                pyAesCrypt.decryptStream(fin, fout, password, buffer_size, enc_file_size)
        except ValueError as e:
            print("An error has occuered %s" % e)
            remove(fileout)


if __name__ == '__main__':
   main()


# python3 ./decrypt.py --filein /Users/alistairknight/Downloads/202206091042.zip.encrypted --fileout /Users/alistairknight/Downloads/202206091042.zip --password 7wq2kNJ4SlXuGyXyzPODMleKs8WtVxp9CvJv4sUBEf8=