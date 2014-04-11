"""
try to convert dae to wrl using meshlabserver.
"""

import sys
import os
import subprocess

import path

overwrite = False
base_dir = path.path(sys.argv[1])
for d in base_dir.dirs():
    dae_fname = d/'model.dae'
    wrl_fname = d/'model.wrl'
    if not overwrite and wrl_fname.exists():
        print 'exists, skipping %s'%(d)
        continue
    cmd = ['meshlabserver', '-i', dae_fname, '-o', wrl_fname]
    print ' '.join(cmd)
    subprocess.call(cmd)
