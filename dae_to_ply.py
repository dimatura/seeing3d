"""
try to convert dae to ply using meshlabserver.
"""

import os
import sys
import subprocess

import path

overwrite = False
base_dir = path.path(sys.argv[1])
for dir_ in base_dir.dirs():
    dae_fname = dir_/'model.dae'
    ply_fname = dir_/'model.ply'
    if not overwrite and ply_fname.exists():
        print 'exists, skipping %s'%(dir_)
        continue
    cmd = ['meshlabserver', '-i', dae_fname, '-o', ply_fname]
    print ' '.join(cmd)
    subprocess.call(cmd)
