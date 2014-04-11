#!/usr/bin/env python

"""
see if normals are plausible by looking at their norm.
"""

import sys
import Image
import numpy as np
import matplotlib.pyplot as pl

img_fname = sys.argv[1]

img = Image.open(img_fname)
imgarr = np.array(img).astype(np.float)/255.
print imgarr.shape
imgarr2 = 2.*imgarr - 1.

imgarr3 = (imgarr2*imgarr2).sum(2)
mask = ~(imgarr3==3.0)
imgarr3 *= mask
imgarr3 = np.sqrt(imgarr3)

print imgarr3.min(), imgarr3.max()

pl.matshow(imgarr3)
pl.colorbar()
pl.show()

#print imgarr2.min(), imgarr2.max()
