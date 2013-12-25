# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

import numpy as np
from matplotlib import pyplot as plt
import ImageDraw, Image
from IPython.core.display import Image as ImageDisplay
import random
from PyQt4.QtGui import QImage, QPainter, QColor, QPolygon
from PyQt4 import Qt
from PyQt4.QtCore import QPoint, QObject

from PyQt4.QtGui import QLabel, QApplication, QPixmap, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog

class Box:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
    
    def grow_to(self, other):
        self.xmin = self.xmin if self.xmin < other.xmin else other.xmin
        self.xmax = self.xmax if self.xmax > other.xmax else other.xmax
        self.ymin = self.ymin if self.ymin < other.ymin else other.ymin
        self.ymax = self.ymax if self.ymax > other.ymax else other.ymax
    
    def fix_aspect_ratio(self, target_ratio):
        target = target_ratio[0] / target_ratio[1]
        current = self.size()[0] / self.size()[1]
        if target > current:
            corr = (self.size()[1] * (target-current))
            self.xmax += 0.5*corr
            self.xmin -= 0.5*corr
        else:
            self.ymax += (self.size()[0] * (current-target))
    
    def __getitem__(self, *args):
        return [[self.xmin, self.xmax], [self.ymin, self.ymax]][args[0]][args[1]]
    
    def size(self):
        return (self.xmax - self.xmin, self.ymax - self.ymin)
    
    def __repr__(self):
        return "({0}, {1}) -> ({2}, {3})".format(self.xmin, self.ymin, self.xmax, self.ymax)

class Branch:
    def __init__(self, position, velocity, params, generation=0):
        self.params = params
        self.position = position
        self.history = [position]
        self.velocity = velocity
        self.branches = []
        self.branch_after = random.randint(*self.params["branch_after_range"])
        self.is_alive = True
        self.is_dying = False
        self.gravity = 0.025
        self.generation = generation
        self.already_drawn = None
    
    def apply_gravity(self):
        weight = np.sin(np.arctan2(np.real(self.velocity), np.imag(self.velocity)))
        accel = self.gravity * np.abs(weight)
        pointing_down = np.imag(self.velocity) < 0
        self.velocity -= complex(0, accel) * (1 if not pointing_down else 3)
        if pointing_down:
            self.velocity = complex(np.real(self.velocity) * 0.94, np.imag(self.velocity) * 0.97)
            if random.randrange(1, 25) == 4:
                self.is_dying = True
    
    def die_if_too_old(self):
        if len(self.history) > 3 and random.randrange(8, 20) < self.generation:
            self.is_alive = False
    
    def grow(self):
        for subbranch in self.branches:
            subbranch.grow()
        
        if np.imag(self.position) < random.randint(12, 40) and np.imag(self.velocity) < 0:
            self.is_alive = False
            
        self.die_if_too_old()
        
        if not self.is_alive:
            return
        
        self.apply_gravity()
        
        self.position += self.velocity
        self.history.append(self.position)

        if len(self.history) > self.branch_after:
            self.is_alive = False
            if self.is_dying:
                return
            v1 = self.velocity - self.params["branch_split"]*(1 + self.params["branch_split_var"] * random.random()-0.5)
            v2 = self.velocity + self.params["branch_split"]*(1 + self.params["branch_split_var"] * random.random()-0.5)
            self.branches.append(Branch(self.position, v1, self.params, self.generation + 1))
            self.branches.append(Branch(self.position, v2, self.params, self.generation + 1))

    def draw_into(self, painter, coordinate_transform, incremental=False):
        for subbranch in self.branches:
            subbranch.draw_into(painter, coordinate_transform, incremental)
        previous = None
        start = self.already_drawn if incremental else None
        points = QPolygon([QPoint(*x) for x in map(coordinate_transform, self.history[start:])])
        if incremental:
            self.already_drawn = len(self.history)
        painter.drawPolyline(points)

    def get_bounding_box(self):
        if len(self.branches) == 0:
            result = Box(
                       min(map(np.real, self.history)),
                       max(map(np.real, self.history)),
                       min(map(np.imag, self.history)),
                       max(map(np.imag, self.history))
                     )
            return result
        children_bounds = [item.get_bounding_box() for item in self.branches]
        own_bounds = Box(0, 0, 0, 0)
        for box in children_bounds:
            own_bounds.grow_to(box)
        return own_bounds
            

class Coordinates:
    def __init__(self, bounding_box, resolution):
        self.bounding_box = bounding_box
        self.resolution = resolution
    
    def __call__(self, *args, **kwargs):
        source_coords = args[0]
        res = (
                (np.real(source_coords) - self.bounding_box.xmin) / self.bounding_box.size()[0] * self.resolution[0],
                self.resolution[1] - (np.imag(source_coords) - self.bounding_box.ymin) / self.bounding_box.size()[1] * self.resolution[1]
              )
        return res

class Tree:
    def __init__(self, params):
        self.trunk = Branch(10, 2.0j, params)
    
    def grow_iterations(self, steps=20, yield_every=0):
        for iteration in range(steps):
            self.trunk.grow()
            if yield_every != 0 and iteration % yield_every == 0:
                yield
    
    def draw(self, existing_image=None, incremental=False, bounding_box=None):
        only_incremental = False
        shape = (400, 400)
        image = QImage(shape[0], shape[1], QImage.Format_RGB32) if existing_image is None else existing_image
        if existing_image is None and not only_incremental:
            image.fill(0)
        if bounding_box is None:
            bounds = self.trunk.get_bounding_box()
            bounds.fix_aspect_ratio(shape)
        else:
            bounds = bounding_box
        coords = Coordinates(bounds, shape)
        painter = QPainter(image)
        painter.setRenderHints(QPainter.HighQualityAntialiasing)
        painter.setPen(QColor(255, 255, 255, 60))
        self.trunk.draw_into(painter, coords, incremental)
        return image

def new_anim():
    image = None
    t = Tree(params = {
            "branch_split": 0.35,
            "branch_after_range": (12, 32),
            "branch_split_var": 1.4,
        })
    for iteration in t.grow_iterations(250, yield_every=5):
        image = t.draw(image, incremental=True, bounding_box=Box(-200, 260, 0, 460))
        pixmap = QPixmap.fromImage(image)
        widget.setPixmap(pixmap)
        widget.repaint()
        QApplication.processEvents()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = QDialog()
    widget = QLabel()
    button = QPushButton("another one!")
    window.setLayout(QVBoxLayout())
    window.layout().addWidget(button)
    window.layout().addWidget(widget)
    button.clicked.connect(new_anim)
    window.show()
    new_anim()
    app.exec_()



