# seeing3d

## Dependencies

- Numpy http://www.numpy.org
- Panda 3D https://www.panda3d.org
- path.py https://pypi.python.org/pypi/path.py
- PIL https://pypi.python.org/pypi/PIL/1.1.6
- termcolor https://pypi.python.org/pypi/termcolor
- Beautiful Soup 3 https://pypi.python.org/pypi/BeautifulSoup/3.2.1

## Rendering models

The main script to render your models into 2D images is ``render.py``. 
The usage syntax is:

```
render.py [-h] [--mode {rgb,depth,normals}] [--win-size WIN_SIZE]
                 [--focal-length-in FOCAL_LENGTH_IN] [--rho-in RHO_IN]
                 [--phi-deg PHI_DEG] [--theta-delta-deg THETA_DELTA_DEG]
                 [--mkdir] [--clear-cache] [--wrl]
                 MODEL_DIR OUTPUT_DIR

Render 3D models to images

positional arguments:
  MODEL_DIR             Base path of model
  OUTPUT_DIR            Model id/directory

optional arguments:
  -h, --help            show this help message and exit
  --mode {rgb,depth,normals}
  --win-size WIN_SIZE   output window size
  --focal-length-in FOCAL_LENGTH_IN
  --rho-in RHO_IN       rho (distance from camera) in inches
  --phi-deg PHI_DEG     phi/pitch in degrees
  --theta-delta-deg THETA_DELTA_DEG
                        theta/yaw increments in degrees
  --mkdir
  --clear-cache
  --wrl                 Use .wrl model. Note: this has no texture
```

For example, 

```
~/render.py ~/chairs/1028b32dc1873c2afe26a3ac360dbd4 ~/tmp_renders
```

would use the default parameters to render 64 RGB views of the model in
directory ``~/chairs/1028b32dc1873c2afe26a3ac360dbd4`` as a sequence of files
in tmp_renders. Note that you will see an empty window pop up, which is a
side-effect of the rendering process.

For a visualization of the phi, theta and rho parameters see the following
figure:

![Camera and model](https://raw.githubusercontent.com/dimatura/seeing3d/master/doc/chair_camera_render.jpg?token=60116__eyJzY29wZSI6IlJhd0Jsb2I6ZGltYXR1cmEvc2VlaW5nM2QvbWFzdGVyL2RvYy9jaGFpcl9jYW1lcmFfcmVuZGVyLmpwZyIsImV4cGlyZXMiOjEzOTgxMTkyOTh9--56522a87fb4438feae3d411e53f9f0c5870aee32)

### How does rendering work?

Conceptually, we set up the scene (including camera, model and lighting),
render the output into a buffer, and save this buffer into a ``.png`` file. In
practice, this involves setting various obscure options in Panda and extreme
care in the format of the Collada model. Unfortunately, libraries to load 3D
models tend to not be very robust. 

You are encouraged to examine and improve the code.

### How to get DAE from SKP? (Added April 8 2015)

If you download the SKP files from warehouse you can't use them directly with this software.
You can convert models manually with sketchup's export feature. 
This obviously doesn't scale well for many models. I wrote a script (``export_dae.rb``)
to export them using the ruby API, which I haven't put here before because it's 
basically a quick hack and I don't know ruby. However, you may still find it useful.


TODO
----

- Warehouse 3D markup changed, breaking scraper.
