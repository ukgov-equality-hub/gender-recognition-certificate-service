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
    args = sys.argv[1:]
    filein = parse_cmd(args, ['-i', '--filein', '--infile'], True)
    fileout = parse_cmd(args, ['-o', '--fileout', '--outfile'], True)
    password = parse_cmd(args, ['-p', '--password'], True)


    if parse_cmd(args, ['help', '-h', '--help'], False):
        print(
            "Simple utility to decrypt S3 backup files\n\n" \
            "Arguments:\n" \
            "--filein       Encrypted filename and location\n" \
            "--fileout      Newly decypted file name and location\n" \
            "--password     The password used to encypt the file\n\n" \
            "Example: ./decrypt.py --filein /Users/<username>/Downloads/202206091042.zip.encrypted --fileout /Users/<username>/Downloads/202206091042.zip --password 123456" \
        )

    else:
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
