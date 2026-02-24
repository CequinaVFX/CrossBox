# coding: utf-8

import os
import sys

import cb_info
import cb_helper as helper


## set scaling factor settings before import any Pyside library
## This might affect some Nuke windows
os.environ["QT_ENABLE_HIGHDPI_SCALING"] =  "1"  # enables auto scaling
os.environ["QT_SCALE_FACTOR"] =  '1'

from Qt import QtCore, QtGui, __binding__
from Qt.QtWidgets import (QApplication, QWidget,  QGroupBox, QFrame, QStyleFactory,
                          QGridLayout, QVBoxLayout, QHBoxLayout, QColorDialog,
                          QPushButton, QLabel, QLineEdit, QCheckBox, QComboBox)
from Qt.QtCore import Qt, Signal, QCoreApplication
from Qt.QtGui import QColor

QGROUPBOX_STYLE = """
    background-color: rgb(64, 64, 64);
"""

KNOB_TOOLTIP = """
  examples:
     size 5 channels alpha
     translate {150, 200}

  Integer:\t5
  Float:\t\t0.5
  Channels:\trgb, alpha
  Bool:\t\ttrue / false
  Color(RGBA):\t{r g b a}
  Box:\t\t{x y r t}
  XY:\t\t{x y}
"""

EMPTY_NODE = {
    "label": "",
    "node_class": "",
    "shortcut": "",
    "knob_values": "",
    "color": "60, 60, 60",
    "inpanel": False
}


def _add_separator(orientation='horizontal', thickness=2, color='60, 60, 60'):
    """
    Args:
        orientation (str): horizontal (default) / vertical
        thickness (int): thickness of the line
        color (str): hex code for color, default is #666 (light-gray)
    Returns:
        QFrame object
    """

    line = QFrame()

    if orientation == 'vertical':
        line.setFrameShape(QFrame.VLine)
    else:
        line.setFrameShape(QFrame.HLine)

    line.setFrameShadow(QFrame.Plain) # (QFrame.Sunken)
    line.setLineWidth(int(thickness))
    line.setMidLineWidth(1)

    line.setStyleSheet("""
        QFrame {
            background-color: rgb('60, 60, 60');
            margin: 10px 0px;
            max-height: 12px;
        }
    """)

    return line


class NodeWidget(QGroupBox):
    node_data = Signal(str, str, str)

    def __init__(self, name=None, parent=None):
        super(NodeWidget, self).__init__(parent)

        # print(button_data)
        # label (lbl, edt)
        # node class (lbl, edt)
        # shortcut (lbl, edt)
        # knob values (lbl, edt)
        # color (btn)
        # open properties (cbx)

        self.setObjectName(name)

        self.got_color = False
        self.default_color = QColor(60, 60, 60)

        glay_main = QGridLayout()
        self.setLayout(glay_main)

        self.btn_get_selected = QPushButton('Get selected')

        lbl_label = QLabel('Label')
        lbl_label.setAlignment(Qt.AlignRight)
        self.edt_label = QLineEdit()
        self.edt_label.setObjectName('edt_label')
        self.edt_label.setToolTip('Give a nice and short name that will be the button name')

        lbl_class = QLabel('Node Class')
        lbl_class.setAlignment(Qt.AlignRight)
        self.edt_class = QLineEdit()
        self.edt_class.setObjectName('edt_class')
        self.edt_class.setToolTip('example: Merge2 Dilate Blur Defocus')

        lbl_shortcut = QLabel('Shortcut')
        lbl_shortcut.setAlignment(Qt.AlignRight)
        self.edt_shortcut = QLineEdit()
        self.edt_shortcut.setObjectName('edt_shortcut')
        self.edt_shortcut.setToolTip('Any single letter - no key combination allowed')
        self.edt_shortcut.setMaxLength(1)

        lbl_knob_values = QLabel('Knob Initial Values')
        lbl_knob_values.setAlignment(Qt.AlignRight)
        self.edt_knob_values = QLineEdit()
        self.edt_knob_values.setObjectName('edt_knob_values')
        self.edt_knob_values.setToolTip(KNOB_TOOLTIP)

        self.btn_color = QPushButton('color')
        self.edt_color = QLineEdit()
        self.edt_color.setObjectName('edt_color')

        self.ckx_open_panel = QCheckBox('open properties panel')
        self.ckx_open_panel.setObjectName('ckx_open_panel')

        glay_main.addWidget(self.btn_get_selected, 0, 0, 1, 2)

        glay_main.addWidget(lbl_label, 1, 0)
        glay_main.addWidget(self.edt_label, 1, 1)

        glay_main.addWidget(lbl_class, 2, 0)
        glay_main.addWidget(self.edt_class, 2, 1)

        glay_main.addWidget(lbl_shortcut, 3, 0)
        glay_main.addWidget(self.edt_shortcut, 3, 1)

        glay_main.addWidget(lbl_knob_values, 4, 0)
        glay_main.addWidget(self.edt_knob_values, 4, 1)

        glay_main.addWidget(self.btn_color, 5, 0)
        glay_main.addWidget(self.edt_color, 5, 1)

        glay_main.addWidget(self.ckx_open_panel, 6, 1)

        self.setStyleSheet(QGROUPBOX_STYLE)

        self.btn_get_selected.clicked.connect(self.get_selected_node)
        self.btn_color.clicked.connect(self.get_color)

        self.edt_label.editingFinished.connect(lambda: self.update_database(self.objectName(),
                                                                            'label',
                                                                            self.edt_label.text()))

        for widget in self.findChildren(QLineEdit):
            widget.editingFinished.connect(lambda w=widget: self.update_database(self.objectName(),
                                                                                 w.objectName().split('_')[-1],
                                                                                 w.text()))

        # self.editingFinished.connect()
        # line_edit.editingFinished.connect(lambda: your_method(line_edit, line_edit.text()))

    def update_values(self, data):
        self.edt_label.setText(data.get('label'))
        self.edt_class.setText(data.get('node_class'))
        self.edt_shortcut.setText(data.get('shortcut'))
        self.edt_knob_values.setText(data.get('knob_values'))
        _color = data.get('color', self.default_color)
        self.edt_color.setText(_color)
        self.update_button_color(_color)
        self.ckx_open_panel.setChecked(data.get('inpanel', False))

    def get_selected_node(self):
        nuke_env = False
        try:
            import cb_nuke_helper as nkh
            nuke_env = True
        except ImportError: pass

        if nuke_env:
            node_data = nkh.get_selected_node()
            if node_data:
                self.update_values(node_data)
        pass

    def get_color(self):
        self.default_color = QColorDialog.getColor()

        if self.default_color.isValid():
            self.got_color = not self.got_color

            _color = '{}, {}, {}'.format(self.default_color.red(),
                                         self.default_color.green(),
                                         self.default_color.blue())

            self.update_button_color(_color)

            self.edt_color.setText(_color)
            self.update_database('color', _color)

    def update_button_color(self, color):
        self.btn_color.setStyleSheet("""
                background-color: rgb({})
                """.format(color))

    def update_database(self, widget_name, data_key, data_value):
        self.node_data.emit(widget_name, data_key, data_value)


class BoxSettings(QWidget):
    selected_box_name = Signal(str)
    delete_box_name = Signal(str)

    def __init__(self, parent=None):
        super(BoxSettings, self).__init__(parent)

        vlay_main = QHBoxLayout()
        self.setLayout(vlay_main)

        glay_widgets = QGridLayout()

        lbl_box_name = QLabel('Box name')
        self.cbx_box_name = QComboBox()
        self.cbx_box_name.setEditable(True)
        self.cbx_box_name.setInsertPolicy(QComboBox.InsertAlphabetically)

        self.btn_delete_box = QPushButton('X')
        self.btn_delete_box.setFixedWidth(24)
        self.btn_delete_box.setStyleSheet('background-color: red')
        self.btn_delete_box.setToolTip('Delete the selected box.')

        lbl_shortcut = QLabel('Box shortcut')
        self.edt_shortcut = QLineEdit()

        glay_widgets.addWidget(lbl_box_name, 0, 0)
        glay_widgets.addWidget(self.cbx_box_name, 0, 1)
        glay_widgets.addWidget(self.btn_delete_box, 0, 2)
        glay_widgets.addWidget(lbl_shortcut, 1, 0)
        glay_widgets.addWidget(self.edt_shortcut, 1, 1)

        glay_widgets.setColumnStretch(0, 1)
        glay_widgets.setColumnStretch(1, 4)
        glay_widgets.setColumnStretch(2, 0)

        vlay_main.addLayout(glay_widgets)

        self.setStyle(QStyleFactory.create('Fusion'))
        # qss_style_content = puts.get_stylesheet()

        self.cbx_box_name.currentIndexChanged.connect(self.changed_box_item)
        self.btn_delete_box.clicked.connect(self.delete_box)

    def update_values(self, new_items):
        self.cbx_box_name.clear()

        for index, (name, shortcut) in enumerate(new_items):
            self.cbx_box_name.addItem(name)

            index = self.cbx_box_name.count() - 1
            model = self.cbx_box_name.model()
            model_index = model.index(index, 0)

            model.setData(model_index, shortcut, QtCore.Qt.UserRole)

        # self.cbx_box_name.setCurrentIndex(0)
        _sh = self.get_selected_task()
        self.edt_shortcut.setText(_sh['shortcut'])

    def get_selected_task(self):
        index = self.cbx_box_name.currentIndex()
        return {
            'box_name': self.cbx_box_name.currentText(),
            'shortcut': self.cbx_box_name.itemData(index, QtCore.Qt.UserRole)
        }

    def changed_box_item(self):
        _item = self.get_selected_task()
        self.edt_shortcut.setText(_item['shortcut'])
        print('changed box item, emiting', _item['box_name'])
        self.selected_box_name.emit(_item['box_name'])

    def delete_box(self):
        _item = self.get_selected_task()
        print('deliting box item, emiting', _item['box_name'])
        self.delete_box_name.emit(_item['box_name'])


class FooterButtons(QFrame):
    def __init__(self, parent=None):
        super(FooterButtons, self).__init__(parent)

        hlay_main = QHBoxLayout()
        self.setLayout(hlay_main)

        self.btn_save = QPushButton('Save')
        self.btn_cancel = QPushButton('Cancel')

        self.btn_save.setFixedHeight(60)
        self.btn_cancel.setFixedHeight(60)

        hlay_main.addWidget(self.btn_save)
        hlay_main.addWidget(self.btn_cancel)


class HelpWidget(QWidget):
    def __init__(self, parent=None):
        super(HelpWidget, self).__init__(parent)

        vlay_main = QVBoxLayout()
        self.setLayout(vlay_main)

        separator = _add_separator()

        hlay_credits = QHBoxLayout()

        _credits = "{} | v{} - {}".format(cb_info.__title__,
                                          cb_info.__version__,
                                          cb_info.__release_date__)
        lbl_credits = QLabel(_credits)

        btn_guide = QPushButton('Guide')
        btn_guide.clicked.connect(self.open_blog)

        hlay_credits.addWidget(lbl_credits)
        hlay_credits.addStretch()
        hlay_credits.addWidget(btn_guide)
        hlay_credits.setContentsMargins(0, 0, 0, 0)

        vlay_main.addWidget(separator)
        vlay_main.addLayout(hlay_credits)
        vlay_main.setContentsMargins(5, 10, 5, 0)

    @staticmethod
    def open_blog():
        """
        Open the CrossBox guide in the default web browser.
        """
        import webbrowser
        webbrowser.open(cb_info.__website_blog__)


class CrossBoxManager(QWidget):
    node_data = Signal(str, str)

    def __init__(self, parent=None):
        super(CrossBoxManager, self).__init__(parent)
        self.database = None
        self.standalone_test = None
        self.nodes_widgets = None
        self.selected_box = None
        self.init_ui()

    def init_ui(self, database=None, standalone_test=False):
        if not database:
            return None

        self.database = database
        self.standalone_test = standalone_test
        self.selected_box = self.find_box_in_database(list(self.database.keys())[0])

        self.box_widget = BoxSettings()

        self.top_node_widget = NodeWidget(name='top_node')
        self.cl_node_widget = NodeWidget(name='cl_node')
        self.cm_node_widget = NodeWidget(name='cm_node')
        self.cr_node_widget = NodeWidget(name='cr_node')
        self.bottom_node_widget = NodeWidget(name='bottom_node')

        self.nodes_widgets = [self.top_node_widget,
                              self.cl_node_widget,
                              self.cm_node_widget,
                              self.cr_node_widget,
                              self.bottom_node_widget]

        for wd in self.nodes_widgets:
            wd.node_data.connect(self.temp_update_db)

        self.footer = FooterButtons()
        self.footer.btn_save.clicked.connect(self.save_database)
        self.footer.btn_cancel.clicked.connect(self.close)

        glay_main = QGridLayout()
        self.setLayout(glay_main)

        glay_main.addWidget(self.box_widget, 0, 1)

        glay_main.addWidget(self.top_node_widget, 1, 1)

        glay_main.addWidget(self.cl_node_widget, 2, 0)
        glay_main.addWidget(self.cm_node_widget, 2, 1)
        glay_main.addWidget(self.cr_node_widget, 2, 2)

        glay_main.addWidget(self.bottom_node_widget, 3, 1)

        glay_main.addWidget(self.footer, 4, 1)

        glay_main.addWidget(HelpWidget(), 5, 0, 1, 3)

        self.populate_boxes_widget()
        self.populate_nodes_widgets()

        # Set Signals from BoxSettings Widget
        self.box_widget.selected_box_name.connect(self.populate_nodes_widgets)
        self.box_widget.delete_box_name.connect(self.delete_box)

        return None

    def populate_boxes_widget(self):
        available_boxes = []
        for box, box_nodes in self.database.items():
            box_name = box.replace('_box', '')
            shortcut = box_nodes.get('settings')['shortcut']
            available_boxes.append((box_name, shortcut))

        self.box_widget.update_values(available_boxes)

    def populate_nodes_widgets(self):
        _box = self.box_widget.get_selected_task()
        self.selected_box = self.find_box_in_database(_box['box_name'])

        for node_box in self.selected_box:
            if node_box == 'top_node':
                top_node = self.selected_box.get('top_node')

                self.top_node_widget.update_values(top_node['tc_button'])

            elif node_box == 'center_nodes':
                center_nodes = self.selected_box.get('center_nodes')
                center_left_node = center_nodes.get('cl_button')
                center_middle_node = center_nodes.get('cc_button')
                center_right_node = center_nodes.get('cr_button')

                self.cl_node_widget.update_values(center_left_node)
                self.cm_node_widget.update_values(center_middle_node)
                self.cr_node_widget.update_values(center_right_node)

            elif node_box == 'bottom_node':
                bottom_nodes = self.selected_box.get('bottom_node')

                self.bottom_node_widget.update_values(bottom_nodes['bc_button'])

    @staticmethod
    def fix_box_name(box_name):
        return box_name if '_box' in box_name else "{}_box".format(box_name)

    def find_box_in_database(self, box_name):
        return self.database.get(self.fix_box_name(box_name), None)

    def update_database(self, box_name):# , delete_box=False):
        # if delete_box:
        #     self.database.pop(self.fix_box_name(box_name))
        #     self.populate_boxes_widget()
        #     self.selected_box = None
        #     return None

        self.selected_box = self.find_box_in_database(box_name)
        if self.selected_box:
            print('update db')
            print(self.selected_box)
        elif box_name == '':
            print('empty box_name, skipping')
            self.selected_box = list(self.database.keys())[0]
            print('selected box', self.selected_box)
        else:
            print('add new box')
            box_name = self.fix_box_name(box_name)
            self.database[box_name] = {
                "settings": {"label": box_name.replace('_box', ''),
                             "shortcut": box_name[0]},
                "top_node": {
                    "tc_button": EMPTY_NODE
                },
                "center_nodes": {
                    "cl_button": EMPTY_NODE,
                    "cc_button": EMPTY_NODE,
                    "cr_button": EMPTY_NODE
                },
                "bottom_node": {
                    "bc_button": EMPTY_NODE
                }
            }
            self.selected_box = self.database[box_name]

    def changed_box_name(self):
        selected_item = self.box_widget.get_selected_task()
        self.update_database(selected_item['box_name'])
        self.populate_nodes_widgets()

    def temp_update_db(self, widget_name, data_key, data_value): # (widget_name, data_key, data_value)
        print('\n\n')
        print('\tDB')
        print(self.database)
        print()
        _box = self.box_widget.get_selected_task()
        print('temp update db', widget_name, data_key, data_value)
        self.selected_box = self.find_box_in_database(_box['box_name'])
        if not _box:
            return
        print('box name', _box)
        node = self.database.get(_box['box_name'])
        print(node)
        # node = box_name.get(widget_name)

        # if not node:
        #     return

        # print(node)

        # db = self.database[box_name]
        # db[data_key] = data_value

    def delete_box(self):
        print('\n\n DELETING GROUP')
        selected_item = self.box_widget.get_selected_task()

        self.database.pop(self.fix_box_name(selected_item['box_name']))
        self.populate_boxes_widget()
        # self.selected_box = None
        # self.update_database(selected_item['box_name'])

    def save_database(self):
        print('saving DB')

    def closeEvent(self, e):
        self.close()
        if self.standalone_test:
            print('Closing standalone')
            QApplication.quit()
        return None


_widget = None
def main():
    global _widget

    if __binding__ == 'PySide2':
        QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    database = helper.load_boxes()

    app_existed = QApplication.instance()# is not None
    app = QApplication.instance() or QApplication(sys.argv)

    _widget = CrossBoxManager()
    _widget.init_ui(database=database, standalone_test=not app_existed)

    _widget.setWindowFlags(Qt.Tool | Qt.Window)

    _widget.show()

    cursor_pos = QtGui.QCursor.pos()
    if hasattr(app, 'desktop'): # PySide2
        desktop = app.desktop()
        screen_num = desktop.screenNumber(cursor_pos)
        screen_rect = desktop.availableGeometry(screen_num)
    else: # PySide6
        # screen_rect = _widget.screen().availableGeometry()
        # if app:
        #     for screen in app.screens():
        #         if screen == app.primaryScreen():
        #             screen_rect = screen.availableGeometry()
        screen_rect = app.primaryScreen().availableGeometry()


    _widget.move(screen_rect.center() - _widget.rect().center())

    _widget.raise_()
    _widget.activateWindow()

    if not app_existed:
        # Run standalone
        app.exec()
        # sys.exit(app.exec() if hasattr(app, "exec") else app.exec_())


if __name__ == '__main__':
    main()