# coding: utf-8
import os
import sys

from cb_helper import load_groups

## set scaling factor settings before import any Pyside library
os.environ["QT_ENABLE_HIGHDPI_SCALING"] =  "1"  # enables auto scaling
os.environ["QT_SCALE_FACTOR"] =  '1'


from Qt import QtCore, QtGui, __binding__
from Qt.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from Qt.QtCore import Qt, Signal, QCoreApplication


# btn_top
# button_center_left
# button_center
# button_center_right
# btn_buttom

# SETTINGS = load_groups('cb_settings')
# {'font_family': 'monospace', 'font_size': 18, 'font_weight': 600, 'ui_scaling_factor': '1.5'}
BTN_STYLESHEET = """
    background-color: rgba({}, .9);
    color: rgb({});
    padding-left: 20px;
    padding-right: 20px;
    font: 18px;
    font-weight: 800;
""" #.format_map(_settings)

HOVER_COLOR = '249, 137, 1' # '247, 211, 125'

def get_contrast_text_color(rgb):
    """
    Get the best readable text color (light or dark) based on the given background color.
    Args:
        rgb (str): the RGB color in the format 'int(R), int(G), int(B)'. Integer values between 0 and 255.
    Returns:
        rgb (str): the RGB color for the text, either light or dark, in the same format as the input.
    """

    LIGHT_TEXT = "180, 180, 180"
    DARK_TEXT = "30, 30, 30"

    rpc = rgb.replace(' ', '')
    rgb_int = [int(value) for value in rpc.split(',')]

    luminance = (0.299 * rgb_int[0] +
                 0.587 * rgb_int[1] +
                 0.114 * rgb_int[2])

    return DARK_TEXT if luminance > 128 else LIGHT_TEXT

class CustomButton(QPushButton):
    def __init__(self, button_name, button_data=None, button_height = 60, parent=None):
        super(CustomButton, self).__init__(parent)

        fixed_button_height = button_height

        label = button_data.get('label')
        shortcut = button_data.get('shortcut', None)
        button_color = button_data.get('color')

        _text_color = get_contrast_text_color(button_color)

        _label = '\n'.join(label.split(' ', 1)) if len(label) > 20 else label
        label = '[ {} ] {}'.format(shortcut.upper(), _label) if shortcut else _label

        self.setObjectName(button_name)
        self.setText(label)
        self.setFixedHeight(fixed_button_height)
        self.setFixedWidth(fixed_button_height * 5)

        # I've discovered by accident, but when you set the property 'shortcut' to a button,
        # it becomes the button's shortcut
        self.setProperty('shortcut', shortcut)
        self.setProperty('node_data', button_data)

        # SETTINGS['background_color'] = button_color
        # SETTINGS['text_color'] = _text_color

        sharpen_corner = 6
        rounded_corner = 30

        stylesheet_map = {
            'btn_top': BTN_STYLESHEET +"""
                border-top-left-radius: {1}px;
                border-top-right-radius: {1}px;
                border-bottom-left-radius: {0}px;
                border-bottom-right-radius: {0}px;
            """.format(sharpen_corner, rounded_corner),
            'btn_left': BTN_STYLESHEET + """
                border-top-left-radius: {1}px;
                border-top-right-radius: {0}px;
                border-bottom-left-radius: {1}px;
                border-bottom-right-radius: {0}px;
            """.format(sharpen_corner, rounded_corner),
            'btn_center': BTN_STYLESHEET + """
                border-top-left-radius: {0}px;
                border-top-right-radius: {0}px;
                border-bottom-left-radius: {0}px;
                border-bottom-right-radius: {0}px;
            """.format(sharpen_corner, rounded_corner),
            'btn_right': BTN_STYLESHEET + """
                border-top-left-radius: {0}px;
                border-top-right-radius: {1}px;
                border-bottom-left-radius: {0}px;
                border-bottom-right-radius: {1}px;
            """.format(sharpen_corner, rounded_corner),
            'btn_bottom': BTN_STYLESHEET + """
                border-top-left-radius: {0}px;
                border-top-right-radius: {0}px;
                border-bottom-left-radius: {1}px;
                border-bottom-right-radius: {1}px;
            """.format(sharpen_corner, rounded_corner),
        }

        self.standard_color = stylesheet_map.get(button_name, '').format(button_color, _text_color)
        self.hover_color = stylesheet_map.get(button_name, '').format(HOVER_COLOR, _text_color)

        self.setStyleSheet(self.standard_color)

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_color)

    def leaveEvent(self, event):
        self.setStyleSheet(self.standard_color)


class CrossBox(QWidget):
    data_submitted = Signal(dict)

    def __init__(self):
        super(CrossBox, self).__init__()
        self.group_data = None
        self.node_data = None
        self.standalone_test = False

    def init_box(self, group_data, standalone_test=False):
        self.group_data = group_data
        self.standalone_test = standalone_test

        collect_buttons = []

        top_group = self.group_data.get('top_group')
        if top_group:
            collect_buttons.append((CustomButton(button_name= 'btn_top', button_data=top_group['tc_button']), (0, 1)))

        center_group = self.group_data.get('center_group')
        collect_buttons.append((CustomButton(button_name= 'btn_left', button_data=center_group['cl_button']), (1, 0)))
        collect_buttons.append((CustomButton(button_name= 'btn_center', button_data=center_group['cc_button']), (1, 1)))
        collect_buttons.append((CustomButton(button_name= 'btn_right', button_data=center_group['cr_button']), (1, 2)))

        bottom_group = self.group_data.get('bottom_group')
        if bottom_group:
            collect_buttons.append((CustomButton(button_name= 'btn_bottom', button_data=bottom_group['bc_button']), (2, 1)))

        glay_main = QGridLayout()
        self.setLayout(glay_main)

        for button, position in collect_buttons:
            button.clicked.connect(self.clicked)
            glay_main.addWidget(button, *position)

        self.setWindowFlags(
            Qt.Popup |
            Qt.FramelessWindowHint |
            Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    ### UI Events
    # Override KeyPressEvent
    def keyPressEvent(self, e):
        # set the Escape key to close the box
        if e.key() == Qt.Key_Escape:
            self.close()
            return None

    # Force closing to avoid infinite loops
    def closeEvent(self, event):
        self.close()
        if self.standalone_test:
            QApplication.quit()
        return None

    ### User interaction
    def clicked(self):
        _data = self.sender().property('node_data')
        self.node_data = _data
        self.data_submitted.emit(_data)
        self.close()


_widget = None
def main(group_data, callback=None):
    global _widget

    if __binding__ == 'PySide2':
        QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app_existed = QApplication.instance() is not None
    app = QApplication.instance() or QApplication(sys.argv)

    _widget = CrossBox()
    _widget.init_box(group_data=group_data, standalone_test=not app_existed)

    if callback:
        # This will send the data to the create_node function in cb_main.py
        _widget.data_submitted.connect(callback)

    _widget.setFocus()
    _widget.activateWindow()
    _widget.show()
    _widget.move(QtGui.QCursor.pos() - _widget.rect().center())
    _widget.raise_()

    if not app_existed:
        # Run standalone to test the interface
        # Needs an venv if PySide2 or 6
        # sys.exit(app.exec() if hasattr(app, "exec") else app.exec_())
        app.exec_()

def print_result(node_data):
    """
    This is an example of the data Widget will send.
    Args:
        node_data (dict): Node_data {
                                'color'         (str):  '160, 55, 120',
                                'node_class'    (str):  'Blur',
                                'shortcut'      (str):  'b',
                                'knob_values'   (str):  'size 15 channels alpha',
                                'label'         (str):  'blur'
                                'inpanel        (bool): 'false'
                                }
    """

    print('\n', '.' * 60)
    print('\t This is an example of the result that you will get from this Widget.')
    print('\t Creating Node:')
    for k, v in node_data.items():
        print("\t\t {}: {}".format(k, v))
    print('.' * 60, '\n')

if __name__ == '__main__':
    crossbox_example = {
        "settings": {"label": "color",
                     "shortcut": "g"},
        "top_group": {
            "tc_button": {
                "label": "colorspace",
                "node_class": "Colorspace",
                "shortcut": "t",
                "knob_values": "",
                "color": "180,180, 180",
                "inpanel": False}
        },
        "center_group": {
            "cl_button": {
                "label": "colorcorrect",
                "node_class": "ColorCorrect",
                "shortcut": "f",
                "knob_values": "channels alpha",
                "color": "145, 145, 145",
                "inpanel": True},
            "cc_button": {
                "label": "grade",
                "node_class": "Grade",
                "shortcut": "g",
                "knob_values": "",
                "color": "151, 152, 15",
                "inpanel": True},
            "cr_button": {
                "label": "saturation",
                "node_class": "Saturation",
                "shortcut": "h",
                "knob_values": "",
                "color": "33, 45, 59",
                "inpanel": True}
        },
        "bottom_group": {
            "bc_button": {
                "label": "grade.alpha",
                "node_class": "Grade",
                "shortcut": "b",
                "knob_values": "channels alpha white_clamp True",
                "color": "33, 45, 59",
                "inpanel": True}
        }
    }

    main(crossbox_example, print_result)
