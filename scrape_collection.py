#!/usr/bin/env python

import time
import os
import urllib2
import sys
import argparse
import cStringIO as StringIO
import shutil
import random
import json
import Image

from BeautifulSoup import BeautifulSoup
import path

import termcolor as tc
import util

# add &start=24 to start later
#collection_url = "http://sketchup.google.com/3dwarehouse/cldetails?mid=48a9c4b69eee43a6dca9b79d6f9077ec"

def download_thumb(mid, fname):
    """ save thumb of model id to fname """
    print tc.colored('downloading '+fname, 'green')
    url = "http://sketchup.google.com/3dwarehouse/details?mid="+mid
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    thumb_elt = soup.find('img', attrs={'id': 'previewImage'})
    img_src = "http://sketchup.google.com"+thumb_elt['src']
    img_data = StringIO.StringIO(urllib2.urlopen(img_src).read())
    img = Image.open(img_data)
    img.save(fname)

def get_download_urls(collection_url):
    """ get download urls for collection """
    ended = False
    download_urls = []
    for s in range(0, 500, 12):
        url = collection_url + '&start=%d'%s
        print 'Scraping model urls from %s, ended: %r'%(url, ended)
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        # urls look like <a class="dwnld" href="/3dwarehouse/download?mid=35ee4bcad88ab50af6e44a01c524295b&rtyp=s8&fn=Untitled&ctyp=other&ts=1332919170000">Download to SketchUp 8</a>
        download_a = soup.findAll('a', attrs={'class' : 'dwnld'})
        if len(download_a)==0:
            ended = True
            break
        for a in download_a:
            print a
            dwnld_url = "http://sketchup.google.com"+a['href']
            if dwnld_url in download_urls:
                # we're cycling
                ended = True
                break
            download_urls.append(dwnld_url)
        if ended:
            break
    time.sleep(1. + 5. * random.random())
    return download_urls

def download_model(dwnld_url, output_dir, get_thumb=True):
    base, rest = dwnld_url.split('?', 1)
    params = dict([param.split('=') for param in rest.split('&')])
    mid = params['mid']
    rtyp = params['rtyp']
    name = params['fn']
    # TODO in theory could be collada or kmz
    sub_output_dir = output_dir/mid
    if not sub_output_dir.exists(): sub_output_dir.mkdir()
    fname = sub_output_dir/'model.skp'
    print tc.colored('downloading '+fname, 'green')
    data = urllib2.urlopen(dwnld_url).read()
    with open(fname, 'wb') as f:
        f.write(data)
    if get_thumb:
        thumb_fname = sub_output_dir/'thumb.3dwarehouse.jpg'
        download_thumb(mid, thumb_fname)
    # upload/create json metadata
    json_fname = sub_output_dir/'metadata.json'
    print tc.colored('saving metadata '+json_fname, 'green')
    data = {'mid': mid, 'rtyp': rtyp, 'name': name}
    util.json_dict_update(json_fname, data)

def download_query(query_url, existing_model_mids, output_dir):
    dwnld_urls = get_download_urls(query_url)
    for dwnld_url in dwnld_urls:
        base, rest = dwnld_url.split('?', 1)
        params = dict([param.split('=') for param in rest.split('&')])
        if not params['mid'] in existing_model_mids:
            download_model(dwnld_url, output_dir)
        else:
            print tc.colored('%s is dupe, skipping'%dwnld_url, 'red')
        time.sleep(1. + 5. * random.random())

def similar_query_url(mid):
    return 'http://sketchup.google.com/3dwarehouse/similar?mid=%s&ct=mdsm'%mid

parser = argparse.ArgumentParser(description='scrape models from warehouse 3D')
parser.add_argument('collection_url', nargs=1, help='URL of collection or query')
parser.add_argument('--dest', '-d', help='Directory to save models')
parser.add_argument('--existing', '-e', help='json with existing model ids to avoid duplication.')
#parser.add_argument('--dry-run', action="store_true", help="Don't download models or images")

args = parser.parse_args()
collection_url = args.collection_url[0]
# clean up collection url
base, rest = collection_url.split('?', 1)
params = dict([param.split('=') for param in rest.split('&')])
collection_url = '?'.join([base, 'mid='+params['mid']])
print tc.colored('Collection URL:', 'green'), tc.colored(collection_url, 'white')

if args.dest:
    output_dir = path.path(args.dest)
else:
    output_dir = path.path('./models')

print tc.colored('output dir:', 'green'), tc.colored(output_dir, 'white')
if not output_dir.exists(): output_dir.mkdir()

if args.existing:
    with open(args.existing) as f:
        existing_model_mids = set(json.load(f))
else:
    args.existing = output_dir/'existing.json'
    existing_model_mids = set()

print '%d existing models'%len(existing_model_mids)

download_query(collection_url, existing_model_mids, output_dir)
# update existing existing_model_mids
model_ids = set(map(str, [d.basename() for d in output_dir.dirs()]))
existing_model_mids = existing_model_mids.union(model_ids)
to_save = sorted(list(existing_model_mids))
print 'updating %s'%args.existing
with open(args.existing, 'w') as f:
    json.dump(to_save, f)
