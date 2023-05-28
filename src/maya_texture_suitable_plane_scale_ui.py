#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2 import QtCore, QtWidgets
import traceback

import maya_texture_suitable_plane_scale as mtsps
reload(mtsps)

WINDOW_TITLE = "textureSuitablePlaneScale"


class TextureSuitablePlaneScaleUI(MayaQWidgetBaseMixin, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TextureSuitablePlaneScaleUI, self).__init__(*args, **kwargs)

        self.setWindowTitle(WINDOW_TITLE)

        self.create_widget()
        self.create_layout()

    def create_widget(self):
        self.requirement_label = QtWidgets.QLabel()
        self.requirement_label.setObjectName("requirement_label")
        self.requirement_label.setText("Requirement: The selected objects must have a material with a texture map connected to the color attribute.")
        self.requirement_label.setAlignment(QtCore.Qt.AlignCenter)
        self.requirement_label.setWordWrap(True)

        self.magnification_label = QtWidgets.QLabel()
        self.magnification_label.setObjectName("_label")
        self.magnification_label.setText("Magnification:")
        self.magnification_label.setAlignment(QtCore.Qt.AlignCenter)

        self.radioButton_buttonGroup = QtWidgets.QButtonGroup()
        self.radioButton_buttonGroup.setObjectName("radioButton_buttonGroup")

        self.radioButton_1 = QtWidgets.QRadioButton()
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButton_1.setText("* 1")
        self.radioButton_buttonGroup.addButton(self.radioButton_1)

        self.radioButton_10 = QtWidgets.QRadioButton()
        self.radioButton_10.setObjectName("radioButton_10")
        self.radioButton_10.setText("* 0.1")
        self.radioButton_buttonGroup.addButton(self.radioButton_10)

        self.radioButton_100 = QtWidgets.QRadioButton()
        self.radioButton_100.setObjectName("radioButton_100")
        self.radioButton_100.setText("* 0.01")
        self.radioButton_100.setChecked(True)
        self.radioButton_buttonGroup.addButton(self.radioButton_100)

        self.radioButton_1000 = QtWidgets.QRadioButton()
        self.radioButton_1000.setObjectName("radioButton_1000")
        self.radioButton_1000.setText("* 0.001")
        self.radioButton_buttonGroup.addButton(self.radioButton_1000)

        self.scale_button = QtWidgets.QPushButton()
        self.scale_button.setObjectName("scale_button")
        self.scale_button.setText("Scale")
        self.scale_button.clicked.connect(mtsps.execute)

    def create_layout(self):
        main_verticalLayout = QtWidgets.QVBoxLayout(self)
        main_verticalLayout.setObjectName("main_verticalLayout")
        main_verticalLayout.addWidget(self.requirement_label)
        main_verticalLayout.addWidget(self.magnification_label)

        magnification_verticalLayout = QtWidgets.QVBoxLayout()
        magnification_verticalLayout.setObjectName("magnification_verticalLayout")
        magnification_verticalLayout.addWidget(self.radioButton_1)
        magnification_verticalLayout.addWidget(self.radioButton_10)
        magnification_verticalLayout.addWidget(self.radioButton_100)
        magnification_verticalLayout.addWidget(self.radioButton_1000)

        magnification_gridLayout = QtWidgets.QGridLayout()
        magnification_gridLayout.setObjectName("magnification_gridLayout")
        magnification_gridLayout.addWidget(self.magnification_label, 0, 1)
        magnification_gridLayout.addLayout(magnification_verticalLayout, 0, 2)
        magnification_gridLayout.setAlignment(QtCore.Qt.AlignCenter)

        main_verticalLayout.addLayout(magnification_gridLayout)

        main_verticalLayout.addWidget(self.scale_button)

def execute():
    """
    Executes the UI.

    Raises:
        Exception: An error occurred.
    """
    try:
        # Check if the window already exists
        if cmds.window(WINDOW_TITLE, exists=True):
            cmds.deleteUI(WINDOW_TITLE)
        # Create the window
        window = TextureSuitablePlaneScaleUI()
        window.show()
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))
        # Print the traceback
        cmds.warning(traceback.format_exc())

if __name__ == "__main__":
    execute()
