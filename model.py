
import sys
import json
import Image

import numpy as np

import path

class Model(object):
    def __init__(self, model_dir):

        self.model_dir = path.path(model_dir)
        self.metadata_path = path.path('metadata.json')
        self.thumb_render_path = path.path('thumb.render.png')
        self.thumb_render_left_path = path.path('thumb.render.left.png')
        self.thumb_3dwarehouse_path = path.path('thumb.3dwarehouse.png')

        if not self.model_dir.isdir():
            raise ValueError('%s is not a directory'%model_dir)

        self.mid = self.model_dir.basename()

        with open(self.model_dir/self.metadata_path) as f:
            self.metadata = json.load(f)

    def load_thumb_render(self):
        self._thumb_render = Image.open(self.model_dir/self.thumb_render_path)

    def load_thumb_render_left(self):
        self._thumb_render_left = Image.open(self.model_dir/self.thumb_render_left_path)

    def load_thumb_3dwarehouse(self):
        self._thumb_3dwarehouse = Image.open(self.model_dir/self.thumb_3dwarehouse_path)

    def save_metadata(self):
        with open(self.model_dir/self.metadata_path, 'w') as f:
            json.dump(self.metadata, f)

    @property
    def thumb_render(self):
        if not hasattr(self, '_thumb_render'):
            self.load_thumb_render()
        return self._thumb_render

    @property
    def thumb_render_left(self):
        if not hasattr(self, '_thumb_render_left'):
            self.load_thumb_render_left()
        return self._thumb_render_left

    @property
    def thumb_3dwarehouse(self):
        if not hasattr(self, '_thumb_3dwarehouse'):
            self.load_thumb_3dwarehouse()
        return self._thumb_3dwarehouse

