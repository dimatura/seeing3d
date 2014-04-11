#!/usr/bin/env python

"""
Get camera matrices
"""

import os
import pprint

import numpy as np
import matplotlib.pyplot as pl
import path

import model

from pandac.PandaModules import *

WIDTH = 600
HEIGHT = 600
FOCAL_LENGTH_IN = 1.37795276 # 35 mm
loadPrcFileData('', 'win-size %d %d'%(WIDTH, HEIGHT))
loadPrcFileData('', 'win-fixed-size #t')

from direct.showbase.ShowBase import ShowBase

def obj_centered_camera_pose(rho_in, phi_deg, theta_deg):
    phi, theta = np.radians((phi_deg, theta_deg))
    x = (rho_in * np.cos(theta) * np.cos(phi))
    y = (rho_in * np.sin(theta) * np.cos(phi))
    z = (rho_in * np.sin(phi))
    base.cam.setPos(x, y, z)
    base.cam.lookAt(Point3(0, 0, 0))

def as_numpy(A):
    a = np.asarray([ [A(i,j) for j in xrange(4)] for i in xrange(4) ] )
    return a

base = ShowBase()
#lens = PerspectiveLens()
#lens.setFov(54.611362) #from sketchup fov
#lens.setFocalLength(FOCAL_LENGTH_IN)
 # TODO can be a parameter
#base.camLens.setFocalLength(FOCAL_LENGTH_IN)
#base.camLens.setFilmSize(0.94499189, 1.41732283)
#base.camLens.setFilmSize(0.94499189)
# so both of these apparently are 36 mm film size
#base.camLens.setFilmSize(1.41732283)

base.camLens.setFov(54.611362) #from sketchup fov
base.camLens.setFocalLength(FOCAL_LENGTH_IN)

#rho_ins = [8*12]
rho_ins = [15*12]
#rho_ins = [60]
phi_degs = [20, 40]
#phi_degs = [20]
theta_degs = np.linspace(0, 360, 32.)
#theta_degs = [0]
total = len(rho_ins)*len(phi_degs)*len(theta_degs)

rho_in = 12*8
phi_deg = 20
theta_deg = 0

obj_centered_camera_pose(12*8, phi_deg, theta_deg)

C = as_numpy(Mat4.convertMat(CSYupRight, base.camLens.getCoordinateSystem()))
P = as_numpy(base.camLens.getProjectionMat())
proj = np.dot(C, P)
print 'proj'
print proj
gsg = base.win.getGsg()
S = as_numpy(Mat4.convertMat(gsg.getCoordinateSystem(), CSYupRight))
V = as_numpy(base.cam.getMat())
M = np.linalg.inv(V)
modelview = np.dot(M, S)
print 'modelview'
print modelview

