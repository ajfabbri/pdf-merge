import os.path
import sys
from pathlib import Path
from typing import Optional

from pypdf import PdfWriter

DEBUG = True


def dprint(s):
    if DEBUG:
        print(f"(debug) {s}")


def merge(fnames: list[str], outname: Optional[str]) -> None:

    if not outname:
        (base, ext) = os.path.splitext(fnames[0])
        ext = ext if ext else ""
        outname = f"{base}-all{ext}"

    outpath = Path(outname)
    if outpath.exists():
        print(f"--> Moving existing {outname} to {outname}.bak")
        outpath.rename(f"{outname}.bak")

    pwriter = PdfWriter()
    for pdf in fnames:
        dprint(f"Appending {pdf}")
        pwriter.append(pdf)
    print(f"==> Writing merged file to {outname}")
    pwriter.write(outname)
    pwriter.close()


def usage():
    print("Usage:")
    print("pdfmerge.py <filename1> <filename2> [<filenames>..]")
    sys.exit()


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        usage()
    for f in args:
        if not os.path.exists(f):
            sys.stderr.write(f"File not found: {f}, exiting.")
            sys.exit()

    merge(args, None)


if __name__ == "__main__":
    main()
