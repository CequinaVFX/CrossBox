import os
import sys

from cb_helper import load_groups
from cb_manager import FooterButtons


from Qt import QtCore, QtGui, __binding__
from Qt.QtWidgets import (QApplication, QWidget,  QGroupBox, QFrame, QStyleFactory,
                          QGridLayout, QVBoxLayout, QHBoxLayout,
                          QPushButton, QLabel, QLineEdit, QCheckBox, QComboBox)
from Qt.QtCore import Qt, Signal, QCoreApplication


class CrossBoxSettings(QWidget):
    def __init__(self, parent=None):
        super(CrossBoxSettings, self).__init__(parent)

        self._settings = load_groups('cb_settings')
        print(self._settings)

    def init_ui(self):

        pass