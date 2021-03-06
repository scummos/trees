# -*- coding: utf-8 -*-

import random

from PyQt4 import Qt
from PyQt4.QtCore import QPoint, QObject, QPointF, QLineF, QEventLoop

from PyQt4.QtGui import QImage, QPainter, QColor, QPolygon
from PyQt4.QtGui import QLabel, QApplication, QPixmap, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog
from PyQt4.QtGui import QPen, QGraphicsScene, QPolygonF, QLinearGradient, QBrush, QPainterPath

import numpy as np

image_shape = (1200, 800)

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

    def enlarge(self, by_percent):
        f = by_percent / 100.0 / 2.0
        self.xmin -= self.size()[0] * f
        self.xmax += self.size()[0] * f
        self.ymin -= self.size()[1] * f
        self.ymax += self.size()[1] * f
    
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
        self.gravity = self.params["gravity"]
        self.generation = generation
        self.already_drawn = None
        self.down_damping_x = self.params["down_damping_x"]
        self.down_damping_y = self.params["down_damping_y"]
    
    def apply_gravity(self):
        weight = np.sin(np.arctan2(np.real(self.velocity), np.imag(self.velocity)))
        accel = self.gravity * np.abs(weight)
        pointing_down = np.imag(self.velocity) < 0
        self.velocity -= complex(0, accel) * (1 if not pointing_down else 3)
        if pointing_down:
            self.velocity = complex(np.real(self.velocity) * self.down_damping_x,
                                    np.imag(self.velocity) * self.down_damping_y)
            if random.randrange(1, self.params["down_die_probability"]) == 4:
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
            if self.params["keep_central"] < random.uniform(0, 1):
                self.is_alive = False
            if self.is_dying:
                return
            self.do_branch()

    def do_branch(self, count=2):
        v1 = self.velocity - self.params["branch_split"]*(1 + self.params["branch_split_var"] * random.random()-0.5)
        v2 = self.velocity + self.params["branch_split"]*(1 + self.params["branch_split_var"] * random.random()-0.5)
        v1 = v1 / np.abs(v1) * np.abs(self.velocity) * random.uniform(0.9, 1.1)
        v2 = v2 / np.abs(v2) * np.abs(self.velocity) * random.uniform(0.9, 1.1)
        self.branches.append(Branch(self.position, v1, self.params, self.generation + 1))
        self.branches.append(Branch(self.position, v2, self.params, self.generation + 1))

    def draw_into(self, scene, incremental=False):
        for subbranch in self.branches:
            subbranch.draw_into(scene, incremental)
        start = self.already_drawn if incremental else None
        points = [QPointF(np.real(x), -np.imag(x)) for x in self.history[start:]]

        gens = float(self.params["painter_generations"])
        scale_factor = (self.params["scale"] - 1) * 3 + 1
        pen_width = max(0, gens-self.generation) / gens * self.params["painter_thickness"] * scale_factor
        if self.generation == 0 and len(self.history) < 30:
            intensity = 126/30.0 * len(self.history)
        else:
            intensity = 17 + 99 * max(0, gens-self.generation) / gens
        color = self.params["color"].darker(85 + (127 - intensity) * 4)
        outline = color.darker(500)
        pen = QPen(color)
        pen.setWidthF(pen_width)
        darkPen = QPen(outline)
        darkPen.setWidthF(pen_width)
        depth = self.params["depth"]
        path = QPainterPath()
        path.moveTo(points[0])
        for index in range(1, len(points) - 1):
            path.lineTo(points[index])
        scene.addPath(path, pen)

        if incremental:
            self.already_drawn = max(0, len(self.history) - 1)

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

class GrassDrawer:
    def __init__(self, view):
        self.view = view
        self.bounds = self.view.scene().itemsBoundingRect()

    def draw_some_grass(self, bundles=100):
        for i in range(bundles):
            width = abs(self.bounds.bottomLeft().x() - self.bounds.bottomRight().x())
            x = random.gauss((self.bounds.bottomLeft().x() + self.bounds.bottomRight().x()) / 2.0, width / 4.5)
            x = max(x, self.bounds.bottomLeft().x() - 1.2*width)
            x = min(x, self.bounds.bottomRight().x() + 1.2*width)
            max_z = 0.35 * (self.bounds.topLeft().y() - self.bounds.bottomLeft().y())
            z = - (random.uniform(0, 1) ** 1.5 - 0.5 + random.uniform(-0.35, 0.35)) * max_z
            size = 0.25 + ((max_z - z) / max_z) ** 1.5 + random.uniform(-0.1, 0.1)
            y = z
            opacity = ((max_z - (z+0.5*max_z)) / max_z) ** 2
            self.draw_grass_bundle(location=(x, y), size=size, items=random.randint(6, 14), opacity=opacity)
            if i % 25 == 0:
                QApplication.processEvents()

    def draw_grass_bundle(self, location, size, items, opacity):
        baseSize = 8
        size = size * baseSize
        baseHeight = 0.4
        pen = QPen(QColor(180, 180, 180, opacity * 80 + 15))
        for i in range(items):
            segments = 5
            exponent = 2.0
            base = QPoint(*location)
            x_diff = size * baseSize * random.uniform(-0.25, 0.25)
            y_diff = size * baseSize * random.uniform(0.8, 1.2) * baseHeight
            current_location = base
            for segment_index in range(segments):
                segment_tip = QPoint(location[0] + x_diff / segments ** exponent * (segment_index + 1) ** exponent,
                                     location[1] - y_diff / segments * segment_index)
                self.view.scene().addLine(QLineF(current_location, segment_tip), pen).setZValue(np.imag(location[0]))
                current_location = segment_tip

class Tree:
    def __init__(self, params, base_location=10, scale=1.0):
        params["scale"] = scale
        params["color"].darker(1/scale * 50)
        params["depth"] = np.imag(base_location)
        self.trunk = Branch(base_location, params["v_start"] * scale, params)
        start = params["start_branches"]
        if start > 1:
            self.trunk.is_alive = False
            for i in range(start / 2):
                self.trunk.do_branch()
            if start % 2 == 1:
                self.trunk.branches[0].is_alive = False
                self.trunk.do_branch()

    def grow_iterations(self, steps=20, yield_every=0):
        for iteration in range(steps):
            self.trunk.grow()
            if yield_every != 0 and iteration % yield_every == 0:
                yield

    def draw(self, scene, incremental=False):
        self.trunk.draw_into(scene, incremental)

class TreeDialog(QDialog):
    def __init__(self):
        import treedialog
        QDialog.__init__(self)
        self.ui = treedialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.draw_buton.clicked.connect(self.new_anim)
        self.scene = QGraphicsScene()
        self.ui.image.setScene(self.scene)
        self.ui.image.setRenderHints(QPainter.HighQualityAntialiasing)

    def get_params(self):
        params = dict()
        params["branch_split"] = self.ui.branch_split.value()
        params["branch_after_range"] = (self.ui.branch_after_min.value(), self.ui.branch_after_max.value())
        params["branch_split_var"] = self.ui.branch_split_var.value()
        params["gravity"] = self.ui.gravity.value()
        params["down_die_probability"] = self.ui.down_die_probability.value()
        params["down_damping_x"] = self.ui.down_damping_x.value()
        params["down_damping_y"] = self.ui.down_damping_x.value()
        params["start_branches"] = self.ui.start_branches.value()
        params["keep_central"] = self.ui.keep_central.value()
        params["color"] = QColor(self.ui.r.value() * 255, self.ui.g.value() * 255, self.ui.b.value() * 255)
        params["color_speed"] = self.ui.color_speed.value()
        params["painter_thickness"] = self.ui.painter_thickness.value()
        params["painter_generations"] = self.ui.painter_generations.value()
        start_rand = [random.uniform(-1, 1) * self.ui.v_start_var.value() for i in range(2)]
        params["v_start"] = complex(self.ui.v_start_x.value()+start_rand[0], self.ui.v_start_y.value()+start_rand[1])
        return params

    def new_anim(self):
        image = None
        painter_id = random.randint(0, 2**32)
        self.active_painer = painter_id
        index = 0
        every = self.ui.repaint.value()

        self.scene.clear()

        tree_count = self.ui.tree_count.value()
        need_spacing = 65
        used_locations = []
        for tree_index in range(tree_count):
            z_range = 80
            base_z = random.uniform(-z_range, z_range)

            def make_base():
                return complex(10 + random.uniform(-350 + 150*tree_count, 350 + 150*tree_count), base_z)
            def closest_distance_to_used(base):
                return min([np.abs(np.real(base - item)) for item in used_locations])
            base_location = make_base()
            while not len(used_locations) == 0 and closest_distance_to_used(base_location) < need_spacing:
                base_location = make_base()

            used_locations.append(base_location)
            scale = 1.0 + 0.75 * ((z_range - base_z) / (2*z_range)) ** 2
            self.tree = Tree(self.get_params(), base_location=base_location, scale=scale)
            for iteration in self.tree.grow_iterations(self.ui.generations.value(), yield_every=every):
                self.tree.draw(self.scene, incremental=True)
                self.ui.progress.setText("Working ... displayed frame: {0}".format(index))

                gradient = QLinearGradient(self.scene.itemsBoundingRect().topLeft(),
                                           self.scene.itemsBoundingRect().bottomLeft())
                gradient.setColorAt(0.4, QColor(0, 0, 0))
                gradient.setColorAt(0, QColor(25, 25, 25))
                self.scene.setBackgroundBrush(QBrush(gradient))

                self.ui.image.repaint()
                QApplication.processEvents()
                index += every
                if self.active_painer != painter_id:
                    return

        self.ui.image.fitInView(self.scene.itemsBoundingRect(), 1)
        d = GrassDrawer(self.ui.image)
        d.draw_some_grass(150 + 75*tree_count)
        #self.ui.image.fitInView(self.scene.itemsBoundingRect(), 1)
        self.ui.progress.setText("Done. Displayed frame: {0}".format(index))

def aboutToQuit():
    # Prevents a crash, probably a bug in pyqt
    window.ui.image.deleteLater()
    window.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = TreeDialog()
    window.show()
    window.new_anim()
    app.setActiveWindow(window)
    app.aboutToQuit.connect(aboutToQuit)
    exit(app.exec_())

