import sys
import subprocess
import pathlib
import argparse

try:
    from PyQt4 import QtGui
    import argparseui
except ImportError:
    print ("Cannot import UI libraries. This python3 tool depends on argparseui and PyQt4")


def mkdir_p(path):
    import errno
    import os
    try:
        os.makedirs("{0}".format(path))
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and path.is_dir():
            pass
        else:
            raise

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", help="folder where zip files are located", type=str,
            default="/home/username/downloads/www.bandshed.net/sounds/sfz")
    parser.add_argument("-r", "--resultfolder", help="folder where zip files will be unzipped", type=str,
            default="/home/username/nobudget/sfz")
    return parser

def setup_app(parser):
    app = QtGui.QApplication(sys.argv)
    a = argparseui.ArgparseUi(parser)
    return a, app

def exit(code, msg):
    print(msg)
    sys.exit(code)

def safe_unzip(options):
    inp = pathlib.Path(options.folder)
    if not inp.exists():
        exit(1, "folder with zip files {0} not found".format(options.folder))

    outp = pathlib.Path(options.resultfolder)
    try:
        mkdir_p(outp)
    except Exception as e:
        exit(2, "couldn't create result folder {0} (reason {1})".format(options.resultfolder, e))

    files = inp.glob("*.zip")
    for f in files:
        filename = f.name[:-len(f.suffix)]
        newdir = outp.joinpath(filename)
        mkdir_p(newdir)
        print ("extract {0} to {1}".format(f, newdir))
        subprocess.check_call(["unzip", "{0}".format(f), "-d", "{0}".format(newdir)])


def main():
    p = setup_parser()
    a, app = setup_app(p)
    a.show()
    app.exec_()
    if a.result() == 1:
        parsed_args = a.parse_args()
        safe_unzip(parsed_args)

if __name__ == '__main__':
    main()
