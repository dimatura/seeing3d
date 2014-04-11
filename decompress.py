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
parser.add_argument('--all', action='store_true')
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
if args.all or args.dae: exts.append('dae')
if args.all or args.wrl: exts.append('wrl')
if args.all or args.ply: exts.append('ply')
if args.verbose:
    pprint.pprint(exts)

#base_dir = path.path(sys.argv[1])
#for d in base_dir.dirs():
for d in dirs:
    for ext in ('wrl', 'ply', 'dae'):
        fname = d/('model.%s.gz'%ext)
        if not fname.exists(): continue
        cmd = ['gunzip', fname]
        print(' '.join(cmd))
        if not args.dry_run:
            subprocess.call(cmd)
