#!/bin/bash
for filename in *.ply; do
    filename_no_ext=$(basename "$filename" .ply)
    ./ply2jpg.py ${filename}
    convert ${filename_no_ext}.png -threshold 50% -define png:color-type=1 -define png:bit-depth=1 ${filename_no_ext}.png
done
