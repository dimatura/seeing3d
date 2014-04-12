#!/usr/bin/env python
"""
Render 3D models from multiple viewpoints and save as .png
"""

import math
import time
import cStringIO as StringIO
import sys
import glob
import os
import json
import argparse
import tempfile
import subprocess
import Image

import numpy as np

import path

import model

parser = argparse.ArgumentParser(description='Render 3D models to images')
parser.add_argument('MODEL_DIR', help='Base path of model')
parser.add_argument('OUTPUT_DIR', help='Model id/directory')
parser.add_argument('--mode', action='store', choices=('rgb', 'depth', 'normals'), default='rgb')
parser.add_argument('--win-size', action='store', type=int, default=600)
parser.add_argument('--focal-length-in', action='store', default=1.37795276)
parser.add_argument('--rho-in', action='append', type=int,
        help='rho (distance from camera) in inches')
parser.add_argument('--phi-deg', action='append', type=int,
        help='phi/pitch in degrees')
parser.add_argument('--theta-delta-deg', action='store', type=int,
        help='theta/yaw increments in degrees', default=32)
parser.add_argument('--mkdir', action='store_true')
parser.add_argument('--clear-cache', action='store_true')
parser.add_argument('--wrl', action='store_true',
        help='Use .wrl model. Note: this has no texture')
args = parser.parse_args()

if args.phi_deg: args.phi_deg = sorted(args.phi_deg)
if args.rho_in: args.rho_in = sorted(args.rho_in)

WIDTH = args.win_size
HEIGHT = args.win_size
FOCAL_LENGTH_IN = args.focal_length_in
FOV_ANGLE_DEG = 54.611362

from pandac.PandaModules import *

loadPrcFileData('', 'win-size %d %d'%(WIDTH, HEIGHT))
loadPrcFileData('', 'win-fixed-size #t')
loadPrcFileData("", "prefer-parasite-buffer #f")
loadPrcFileData('', 'model-path '+args.MODEL_DIR)

from direct.showbase.ShowBase import ShowBase

def setup():
    global base
    global alt_buffer
    global alt_render
    global alt_texture
    global alt_cam
    base = ShowBase()
    winprops = WindowProperties.size(2*WIDTH, 2*HEIGHT)
    props = FrameBufferProperties()
    props.setRgbColor(1)
    props.setAlphaBits(1)
    props.setDepthBits(1)
    alt_buffer = base.graphicsEngine.makeOutput(base.pipe, "offscreenBuffer",
        -200, props, winprops,
        GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BFRefuseWindow,
        base.win.getGsg(), base.win)
    alt_texture = Texture()
    alt_texture.setMinfilter(Texture.FTLinear)
    alt_texture.setFormat(Texture.FRgba32)
    alt_buffer.addRenderTexture(alt_texture, GraphicsOutput.RTMCopyRam)
    alt_cam = base.makeCamera(alt_buffer)
    alt_buffer.setClearColor(VBase4(1.0,1.0,1.0,1.0))
    alt_render= NodePath("new render")
    if args.mode=='rgb':
        pass
    elif args.mode=='normals':
        shader = Shader.load(Shader.SLGLSL, 'shaders/normrgb.vert', 'shaders/normrgb.frag')
        alt_render.setShader(shader)
    elif args.mode=='depth':
        shader = Shader.load(Shader.SLGLSL, 'shaders/depth.vert', 'shaders/depth.frag')
        alt_render.setShader(shader)
    alt_render.setAntialias(AntialiasAttrib.MMultisample)

    lens = PerspectiveLens()
    lens.setFov(FOV_ANGLE_DEG)
    lens.setFocalLength(FOCAL_LENGTH_IN)
    alt_cam.node().setLens(lens)
    alt_cam.node().setScene(alt_render)

def load_model():
    model_dir = path.path(args.MODEL_DIR)

    if not args.wrl:
        daepath = (model_dir/('model.dae'))
        compressed = False
        if (not os.path.exists(daepath) and os.path.exists(daepath+'.gz')):
            subprocess.check_call(['gunzip', daepath+'.gz'])
            compressed = True
        (fd, eggpath) = tempfile.mkstemp(suffix='.egg')
        os.close(fd)
        subprocess.check_call(['dae2egg', '-o', eggpath, daepath])
        print('loading %s'%daepath)
        model = loader.loadModel(eggpath)
        os.remove(eggpath)
        if compressed: subprocess.check_call(['gzip', daepath])
    else:
        wrlpath = (model_dir/('model.wrl'))
        print('loading %s'%wrlpath)
        model = loader.loadModel(wrlpath)

    with open(model_dir/'metadata.json') as f:
        metadata = json.load(f)
    center = metadata['bb_center'] # unit inches
    model.setPos(-center[0], -center[1], -center[2])
    # TODO this is a bit of a hack.
    if args.wrl:
        model.setHpr(0, -90, 0)
    model.reparentTo(alt_render)

def lighting():
    # TODO lighting should be configurable
    alight = AmbientLight('alight')
    alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
    alnp = alt_render.attachNewNode(alight)
    alt_render.setLight(alnp)
    dlight = DirectionalLight('dlight')
    dlight.setColor(VBase4(0.8, 0.8, 0.8, 1))
    dlnp = alt_render.attachNewNode(dlight)
    dlnp.setHpr(0, -60, 0)
    alt_render.setLight(dlnp)
    base.setBackgroundColor(1,1,1)

def render_to_file(fname):
    alt_texture.clear()
    base.graphicsEngine.renderFrame()
    base.graphicsEngine.renderFrame()
    #base.graphicsEngine.extractTextureData(tex, base.win.getGsg())
    #tex = alt_buffer.getTexture()
    pnm = PNMImage()
    #base.win.getScreenshot(pnm)
    alt_texture.store(pnm)
    ss = StringStream()
    pnm.write(ss, 'pnm')
    sio = StringIO.StringIO(ss.getData())
    img = Image.open(sio)
    # poor man's antialiasing
    img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    img.save(fname)

def obj_centered_camera_pose(rho_in, phi_deg, theta_deg):
    phi, theta = np.radians((phi_deg, theta_deg))
    # spherical coordinates
    x = (rho_in * np.cos(theta) * np.cos(phi))
    y = (rho_in * np.sin(theta) * np.cos(phi))
    z = (rho_in * np.sin(phi))
    base.cam.setPos(x, y, z)
    base.cam.lookAt(Point3(0, 0, 0))
    alt_cam.setPos(x, y, z)
    alt_cam.lookAt(Point3(0, 0, 0))

def main():
    # workaround for panda3d bug
    # TODO has this been fixed yet by panda devs?
    if args.clear_cache:
        map(os.unlink, glob.glob(os.path.join(os.environ['HOME'], '.panda3d', 'cache', '*')))
    setup()
    load_model()
    lighting()
    base.camLens.setFov(FOV_ANGLE_DEG)
    base.camLens.setFocalLength(FOCAL_LENGTH_IN)

    rho_ins = [96] if (args.rho_in is None) else args.rho_in
    phi_degs = [20, 40] if (args.phi_deg is None) else args.phi_deg
    theta_delta_deg = 32 if (args.theta_delta_deg is None) else args.theta_delta_deg
    theta_degs = np.linspace(0, 360, theta_delta_deg).astype(np.int)
    total = len(rho_ins)*len(phi_degs)*len(theta_degs)

    model_dir = path.path(args.MODEL_DIR)
    m = model.Model(model_dir)
    init_theta_deg = m.metadata['orientation_theta_deg']

    dirname = path.path(args.OUTPUT_DIR)
    if not dirname.exists():
        if args.mkdir:
            dirname.mkdir()
        else:
            print 'Error: output directory does not exist'
            return


    k = 0
    for rho_in in rho_ins:
        for phi_deg in phi_degs:
            for theta_deg in theta_degs:
                obj_centered_camera_pose(rho_in, phi_deg, (theta_deg+init_theta_deg)%360 )
                fname = dirname/('image_%03d_p%03d_t%03d_r%03d.png'%(k, phi_deg, theta_deg, rho_in))
                print '%d/%d %s'%(k+1, total, fname); sys.stdout.flush()
                render_to_file(fname)
                k += 1
    print 'finished'

if __name__ == '__main__':
    main()
