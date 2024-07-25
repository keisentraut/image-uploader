#!/usr/bin/python3
# remove all identical files in a directory except the one with shortest file name

import sys
import hashlib
from pathlib import Path

p=Path(sys.argv[1])
files = {}
for filename in p.glob('*'):
    if not filename.is_dir():
        with open(filename, "rb") as f:
            h=hashlib.sha256()
            while chunk := f.read(8192):
                h.update(chunk)
        h=h.hexdigest()
    if h in files:
        files[h].append(filename)
    else:
        files[h] = [filename]
        
for h in files:
    if len(files[h])>1:
        names=sorted(files[h], key=lambda x: len(str(x)))
        print(f"# keep {names[0]}")
        for i in names[1:]:
            print(f"rm -v {i} # same as {names[0]}")
        print()

