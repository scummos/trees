# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'treedialog.ui'
#
# Created: Wed Dec 25 21:00:05 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(926, 761)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.branch_split = QtGui.QDoubleSpinBox(Dialog)
        self.branch_split.setSingleStep(0.05)
        self.branch_split.setProperty("value", 0.3)
        self.branch_split.setObjectName(_fromUtf8("branch_split"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.branch_split)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.branch_after_min = QtGui.QSpinBox(Dialog)
        self.branch_after_min.setSingleStep(4)
        self.branch_after_min.setProperty("value", 24)
        self.branch_after_min.setObjectName(_fromUtf8("branch_after_min"))
        self.horizontalLayout.addWidget(self.branch_after_min)
        self.branch_after_max = QtGui.QSpinBox(Dialog)
        self.branch_after_max.setMaximum(200)
        self.branch_after_max.setSingleStep(4)
        self.branch_after_max.setProperty("value", 44)
        self.branch_after_max.setObjectName(_fromUtf8("branch_after_max"))
        self.horizontalLayout.addWidget(self.branch_after_max)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.branch_split_var = QtGui.QDoubleSpinBox(Dialog)
        self.branch_split_var.setSingleStep(0.1)
        self.branch_split_var.setProperty("value", 2.4)
        self.branch_split_var.setObjectName(_fromUtf8("branch_split_var"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.branch_split_var)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.gravity = QtGui.QDoubleSpinBox(Dialog)
        self.gravity.setDecimals(4)
        self.gravity.setMinimum(-5.0)
        self.gravity.setMaximum(5.0)
        self.gravity.setSingleStep(0.0025)
        self.gravity.setProperty("value", 0.025)
        self.gravity.setObjectName(_fromUtf8("gravity"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.gravity)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label)
        self.generations = QtGui.QSpinBox(Dialog)
        self.generations.setMaximum(1000)
        self.generations.setSingleStep(10)
        self.generations.setProperty("value", 330)
        self.generations.setObjectName(_fromUtf8("generations"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.generations)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_6)
        self.repaint = QtGui.QSpinBox(Dialog)
        self.repaint.setMinimum(1)
        self.repaint.setMaximum(250)
        self.repaint.setProperty("value", 5)
        self.repaint.setObjectName(_fromUtf8("repaint"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.repaint)
        self.label_20 = QtGui.QLabel(Dialog)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_20)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.r = QtGui.QDoubleSpinBox(Dialog)
        self.r.setDecimals(2)
        self.r.setMaximum(1.0)
        self.r.setSingleStep(0.05)
        self.r.setProperty("value", 1.0)
        self.r.setObjectName(_fromUtf8("r"))
        self.horizontalLayout_10.addWidget(self.r)
        self.g = QtGui.QDoubleSpinBox(Dialog)
        self.g.setMaximum(1.0)
        self.g.setSingleStep(0.05)
        self.g.setProperty("value", 1.0)
        self.g.setObjectName(_fromUtf8("g"))
        self.horizontalLayout_10.addWidget(self.g)
        self.b = QtGui.QDoubleSpinBox(Dialog)
        self.b.setMaximum(1.0)
        self.b.setSingleStep(0.05)
        self.b.setProperty("value", 1.0)
        self.b.setObjectName(_fromUtf8("b"))
        self.horizontalLayout_10.addWidget(self.b)
        self.color_speed = QtGui.QDoubleSpinBox(Dialog)
        self.color_speed.setEnabled(False)
        self.color_speed.setMaximum(20.0)
        self.color_speed.setSingleStep(0.5)
        self.color_speed.setProperty("value", 0.5)
        self.color_speed.setObjectName(_fromUtf8("color_speed"))
        self.horizontalLayout_10.addWidget(self.color_speed)
        self.formLayout_2.setLayout(7, QtGui.QFormLayout.FieldRole, self.horizontalLayout_10)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_3.addWidget(self.label_8)
        self.down_damping_x = QtGui.QDoubleSpinBox(Dialog)
        self.down_damping_x.setMaximum(5.0)
        self.down_damping_x.setSingleStep(0.01)
        self.down_damping_x.setProperty("value", 0.95)
        self.down_damping_x.setObjectName(_fromUtf8("down_damping_x"))
        self.horizontalLayout_3.addWidget(self.down_damping_x)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_3.addWidget(self.label_9)
        self.down_damping_y = QtGui.QDoubleSpinBox(Dialog)
        self.down_damping_y.setMaximum(5.0)
        self.down_damping_y.setSingleStep(0.01)
        self.down_damping_y.setProperty("value", 0.97)
        self.down_damping_y.setObjectName(_fromUtf8("down_damping_y"))
        self.horizontalLayout_3.addWidget(self.down_damping_y)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_10)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_4.addWidget(self.label_11)
        self.v_start_x = QtGui.QDoubleSpinBox(Dialog)
        self.v_start_x.setSingleStep(0.1)
        self.v_start_x.setProperty("value", 0.15)
        self.v_start_x.setObjectName(_fromUtf8("v_start_x"))
        self.horizontalLayout_4.addWidget(self.v_start_x)
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_4.addWidget(self.label_12)
        self.v_start_y = QtGui.QDoubleSpinBox(Dialog)
        self.v_start_y.setSingleStep(0.1)
        self.v_start_y.setProperty("value", 2.0)
        self.v_start_y.setObjectName(_fromUtf8("v_start_y"))
        self.horizontalLayout_4.addWidget(self.v_start_y)
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_4.addWidget(self.label_13)
        self.v_start_var = QtGui.QDoubleSpinBox(Dialog)
        self.v_start_var.setSingleStep(0.1)
        self.v_start_var.setProperty("value", 0.2)
        self.v_start_var.setObjectName(_fromUtf8("v_start_var"))
        self.horizontalLayout_4.addWidget(self.v_start_var)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_14)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_6.addWidget(self.label_15)
        self.down_die_probability = QtGui.QSpinBox(Dialog)
        self.down_die_probability.setMinimum(1)
        self.down_die_probability.setMaximum(500)
        self.down_die_probability.setProperty("value", 25)
        self.down_die_probability.setObjectName(_fromUtf8("down_die_probability"))
        self.horizontalLayout_6.addWidget(self.down_die_probability)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_16 = QtGui.QLabel(Dialog)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_16)
        self.down_additional_gravity = QtGui.QDoubleSpinBox(Dialog)
        self.down_additional_gravity.setProperty("value", 3.0)
        self.down_additional_gravity.setObjectName(_fromUtf8("down_additional_gravity"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.down_additional_gravity)
        self.label_17 = QtGui.QLabel(Dialog)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_17)
        self.label_18 = QtGui.QLabel(Dialog)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_18)
        self.start_branches = QtGui.QSpinBox(Dialog)
        self.start_branches.setMinimum(1)
        self.start_branches.setProperty("value", 1)
        self.start_branches.setObjectName(_fromUtf8("start_branches"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.start_branches)
        self.keep_central = QtGui.QDoubleSpinBox(Dialog)
        self.keep_central.setMaximum(1.0)
        self.keep_central.setSingleStep(0.05)
        self.keep_central.setObjectName(_fromUtf8("keep_central"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.keep_central)
        self.label_19 = QtGui.QLabel(Dialog)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_19)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.painter_thickness = QtGui.QDoubleSpinBox(Dialog)
        self.painter_thickness.setDecimals(1)
        self.painter_thickness.setMinimum(0.1)
        self.painter_thickness.setMaximum(50.0)
        self.painter_thickness.setSingleStep(0.5)
        self.painter_thickness.setProperty("value", 5.0)
        self.painter_thickness.setObjectName(_fromUtf8("painter_thickness"))
        self.horizontalLayout_9.addWidget(self.painter_thickness)
        self.painter_generations = QtGui.QSpinBox(Dialog)
        self.painter_generations.setMinimum(1)
        self.painter_generations.setMaximum(1000)
        self.painter_generations.setProperty("value", 8)
        self.painter_generations.setObjectName(_fromUtf8("painter_generations"))
        self.horizontalLayout_9.addWidget(self.painter_generations)
        self.formLayout.setLayout(8, QtGui.QFormLayout.FieldRole, self.horizontalLayout_9)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.draw_buton = QtGui.QPushButton(Dialog)
        self.draw_buton.setObjectName(_fromUtf8("draw_buton"))
        self.horizontalLayout_7.addWidget(self.draw_buton)
        self.progress = QtGui.QLabel(Dialog)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.horizontalLayout_7.addWidget(self.progress)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.image = QtGui.QGraphicsView(Dialog)
        self.image.setObjectName(_fromUtf8("image"))
        self.verticalLayout.addWidget(self.image)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "branch_split: branch split angle", None))
        self.label_3.setText(_translate("Dialog", "branch_after_range: time before branch", None))
        self.label_4.setText(_translate("Dialog", "branch_split_var: split angle variance", None))
        self.label_5.setText(_translate("Dialog", "gravity: pull down branches", None))
        self.label.setText(_translate("Dialog", "do generations", None))
        self.label_6.setText(_translate("Dialog", "repaint every", None))
        self.label_20.setText(_translate("Dialog", "color base + walk speed", None))
        self.label_7.setText(_translate("Dialog", "down_damping: when branch down", None))
        self.label_8.setText(_translate("Dialog", "x", None))
        self.label_9.setText(_translate("Dialog", "y", None))
        self.label_10.setText(_translate("Dialog", "v_start: velocity of trunk", None))
        self.label_11.setText(_translate("Dialog", "x", None))
        self.label_12.setText(_translate("Dialog", "y", None))
        self.label_13.setText(_translate("Dialog", "var", None))
        self.label_14.setText(_translate("Dialog", "down_die_probability", None))
        self.label_15.setText(_translate("Dialog", "chance of 1 in", None))
        self.label_16.setText(_translate("Dialog", "down_additional_gravity_factor", None))
        self.label_17.setText(_translate("Dialog", "start branches", None))
        self.label_18.setText(_translate("Dialog", "keep central alive probability", None))
        self.label_19.setText(_translate("Dialog", "painter thickness / generations", None))
        self.draw_buton.setText(_translate("Dialog", "Redraw", None))
        self.progress.setText(_translate("Dialog", "Done.", None))
