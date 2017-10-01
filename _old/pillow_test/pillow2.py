"""
Run this script with the image filenames as arguments.
example: python pillow2.py image.jpg
"""
import os, sys
from PIL import Image

SIZE = (128, 128)

print("Pillow test script starting...")

for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + "_thumb.jpg"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(SIZE)
            im.save(outfile, "JPEG")
            print(outfile, " saved!")
            print(im.format, im.size, im.mode)
        except IOError:
            print("cannot create thumbnail for", infile)

print("Pillow test script finished...")
