#!/usr/bin/env python
"""
decompress models. alternative: use gzip `find -iname *.dae`
"""

import os
import sys
import subprocess
import pprint
import argparse

import path

parser = argparse.ArgumentParser()
parser.add_argument('model_dir', nargs='+', action='store')
parser.add_argument('--dae', action='store_true')
parser.add_argument('--wrl', action='store_true')
parser.add_argument('--ply', action='store_true')
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--dry-run', '-n', action='store_true')

args = parser.parse_args()

dirs = map(path.path, args.model_dir)
if args.verbose:
    pprint.pprint(dirs)

exts = []
if args.dae: exts.append('dae')
if args.wrl: exts.append('wrl')
if args.ply: exts.append('ply')
if len(exts)==0: exts.extend(['dae', 'wrl', 'ply'])

if args.verbose:
    pprint.pprint(exts)

#base_dir = path.path(sys.argv[1])
#for d in base_dir.dirs():
for d in dirs:
    for ext in exts:
        fname = d/('model.%s.gz'%ext)
        if not fname.exists(): continue
        cmd = ['gunzip', fname]
        print(' '.join(cmd))
        if not args.dry_run:
            subprocess.call(cmd)
