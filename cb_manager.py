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
                          QGridLayout, QVBoxLayout, QHBoxLayout,
                          QPushButton, QLabel, QLineEdit, QCheckBox, QComboBox)
from Qt.QtCore import Qt, Signal, QCoreApplication


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


def create_thick_separator(orientation='horizontal', thickness=2, color='#666'):
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

    line.setFrameShadow(QFrame.Plain)# (QFrame.Sunken)
    line.setLineWidth(int(thickness))
    line.setMidLineWidth(1)

    line.setStyleSheet("""
        QFrame {
            background-color: #666;
            margin: 10px 0px;
            max-height: 2px;
        }
    """)
    return line


class NodeWidget(QGroupBox):
    def __init__(self, parent=None):
        super(NodeWidget, self).__init__(parent)

        glay_main = QGridLayout()
        self.setLayout(glay_main)

        # print(button_data)
        # label (lbl, edt)
        # node class (lbl, edt)
        # shortcut (lbl, edt)
        # knob values (lbl, edt)
        # color (btn)
        # open properties (cbx)

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

    def update_values(self, data):
        self.edt_label.setText(data.get('label'))
        self.edt_class.setText(data.get('node_class'))
        self.edt_shortcut.setText(data.get('shortcut'))
        self.edt_knob_values.setText(data.get('knob_values'))
        self.edt_color.setText(data.get('color', '60, 60, 60'))
        self.ckx_open_panel.setChecked(data.get('inpanel', False))

    def get_selected_node(self):
        # node_data = nkh.get_selected_node()
        # if node_data:
        #     self.update_values(node_data)
        pass


class GroupInfo(QWidget):
    selected_group_name = Signal(str)
    delete_group_name = Signal(str)

    def __init__(self, parent=None):
        super(GroupInfo, self).__init__(parent)

        vlay_main = QHBoxLayout()
        self.setLayout(vlay_main)

        glay_widgets = QGridLayout()

        lbl_group_name = QLabel('Group name')
        self.cbx_group_name = QComboBox()
        self.cbx_group_name.currentIndexChanged.connect(self.changed_group)
        self.cbx_group_name.setEditable(True)
        self.cbx_group_name.setInsertPolicy(QComboBox.InsertAlphabetically)

        self.btn_delete_group = QPushButton('X')
        self.btn_delete_group.setFixedWidth(24)
        self.btn_delete_group.setStyleSheet('background-color: red')
        self.btn_delete_group.setToolTip('Delete the selected group.')
        self.btn_delete_group.clicked.connect(self.delete_group)

        lbl_shortcut = QLabel('Group shortcut')
        self.edt_shortcut = QLineEdit()

        glay_widgets.addWidget(lbl_group_name, 0, 0)
        glay_widgets.addWidget(self.cbx_group_name, 0, 1)
        glay_widgets.addWidget(self.btn_delete_group, 0, 2)
        glay_widgets.addWidget(lbl_shortcut, 1, 0)
        glay_widgets.addWidget(self.edt_shortcut, 1, 1)

        glay_widgets.setColumnStretch(0, 1)
        glay_widgets.setColumnStretch(1, 4)
        glay_widgets.setColumnStretch(2, 0)

        vlay_main.addLayout(glay_widgets)

        self.setStyle(QStyleFactory.create('Fusion'))
        # qss_style_content = puts.get_stylesheet()

    def update_values(self, new_items):
        self.cbx_group_name.clear()

        for index, (name, shortcut) in enumerate(new_items):
            self.cbx_group_name.addItem(name)

            index = self.cbx_group_name.count() - 1
            model = self.cbx_group_name.model()
            model_index = model.index(index, 0)

            model.setData(model_index, shortcut, QtCore.Qt.UserRole)

        # self.cbx_group_name.setCurrentIndex(0)
        _sh = self.get_selected_task()
        self.edt_shortcut.setText(_sh['shortcut'])

    def get_selected_task(self):
        index = self.cbx_group_name.currentIndex()
        return {
            'group_name': self.cbx_group_name.currentText().replace(' ', '_'),
            'shortcut': self.cbx_group_name.itemData(index, QtCore.Qt.UserRole)
        }

    def changed_group(self):
        _item = self.get_selected_task()
        self.edt_shortcut.setText(_item['shortcut'])
        self.selected_group_name.emit(_item['group_name'])

    def delete_group(self):
        _item = self.get_selected_task()
        self.delete_group_name.emit(_item['group_name'])


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

        separator = create_thick_separator()

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
    def __init__(self, parent=None):
        super(CrossBoxManager, self).__init__(parent)
        self.database = None
        self.standalone_test = None
        self.nodes_widgets = None
        self.selected_group = None
        self.init_ui()

    def init_ui(self, database=None, standalone_test=False):
        if not database:
            return None

        self.database = database
        self.standalone_test = standalone_test
        self.selected_group = list(self.database.keys())[0]

        self.group_widget = GroupInfo()
        self.group_widget.selected_group_name.connect(self.changed_group_name)
        self.group_widget.delete_group_name.connect(self.delete_group)

        self.top_node_widget = NodeWidget()
        self.cl_node_widget = NodeWidget()
        self.cm_node_widget = NodeWidget()
        self.cr_node_widget = NodeWidget()
        self.bottom_node_widget = NodeWidget()

        self.nodes_widgets = [self.top_node_widget,
                              self.cl_node_widget,
                              self.cm_node_widget,
                              self.cr_node_widget,
                              self.bottom_node_widget]

        self.footer = FooterButtons()
        self.footer.btn_save.clicked.connect(self.save_database)
        self.footer.btn_cancel.clicked.connect(self.close)

        glay_main = QGridLayout()
        self.setLayout(glay_main)

        glay_main.addWidget(self.group_widget, 0, 1)

        glay_main.addWidget(self.top_node_widget, 1, 1)

        glay_main.addWidget(self.cl_node_widget, 2, 0)
        glay_main.addWidget(self.cm_node_widget, 2, 1)
        glay_main.addWidget(self.cr_node_widget, 2, 2)

        glay_main.addWidget(self.bottom_node_widget, 3, 1)

        glay_main.addWidget(self.footer, 4, 1)

        glay_main.addWidget(HelpWidget(), 5, 0, 1, 3)

        self.populate_groups_widget()
        self.populate_nodes_widgets()

    def populate_groups_widget(self):
        available_groups = []
        print('\n populating group combobox')
        for group, group_nodes in self.database.items():
            group_name = group.replace('_group', '')
            shortcut = group_nodes.get('settings')['shortcut']
            print(group_name, shortcut)
            available_groups.append((group_name, shortcut))

        self.group_widget.update_values(available_groups)
        print('end of populate groups\n')

    def populate_nodes_widgets(self):
        for node_group in self.selected_group:
            if node_group == 'settings':
                continue

            elif node_group == 'top_group':
                top_node = self.selected_group.get('top_group')
                self.top_node_widget.update_values(top_node['tc_button'])

            elif node_group == 'center_group':
                center_nodes = self.selected_group.get('center_group')
                center_left_node = center_nodes.get('cl_button')
                center_middle_node = center_nodes.get('cc_button')
                center_right_node = center_nodes.get('cr_button')

                self.cl_node_widget.update_values(center_left_node)
                self.cm_node_widget.update_values(center_middle_node)
                self.cr_node_widget.update_values(center_right_node)

            else:
                bottom_nodes = self.selected_group.get('bottom_group')
                self.bottom_node_widget.update_values(bottom_nodes['bc_button'])

    @staticmethod
    def fix_group_name(group_name):
        return group_name if '_group' in group_name else "{}_group".format(group_name)

    def find_group_in_database(self, group_name):
        return self.database.get(self.fix_group_name(group_name), None)

    def update_database(self, group_name):# , delete_group=False):
        # if delete_group:
        #     self.database.pop(self.fix_group_name(group_name))
        #     self.populate_groups_widget()
        #     self.selected_group = None
        #     return None

        self.selected_group = self.find_group_in_database(group_name)
        print('group name', group_name)
        if self.selected_group:
            print('update db')
            print(self.selected_group)
        elif group_name == '':
            print('empty group_name, skipping')
            self.selected_group = list(self.database.keys())[0]
            print('selected group', self.selected_group)
        else:
            print('add new group')
            group_name = group_name if '_group' in group_name else "{}_group".format(group_name)
            self.database[group_name] = {
                "settings": {"label": group_name.replace('_group', ''),
                             "shortcut": group_name[0]},
                "top_group": {
                    "tc_button": EMPTY_NODE
                },
                "center_group": {
                    "cl_button": EMPTY_NODE,
                    "cc_button": EMPTY_NODE,
                    "cr_button": EMPTY_NODE
                },
                "bottom_group": {
                    "bc_button": EMPTY_NODE
                }
            }
            self.selected_group = self.database[group_name]

    def changed_group_name(self):
        selected_item = self.group_widget.get_selected_task()
        self.update_database(selected_item['group_name'])
        self.populate_nodes_widgets()

    def delete_group(self):
        print('\n\n DELETING GROUP')
        selected_item = self.group_widget.get_selected_task()

        self.database.pop(self.fix_group_name(selected_item['group_name']))
        self.populate_groups_widget()
        # self.selected_group = None

        # self.update_database(selected_item['group_name'])

    def save_database(self):
        print('saving DB')

    def closeEvent(self, e):
        self.close()
        if self.standalone_test:
            QApplication.quit()
        return None


_widget = None
def main():
    global _widget

    if __binding__ == 'PySide2':
        QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    database = helper.load_groups()

    app_existed = QApplication.instance() is not None
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
        screen_rect = _widget.screen().availableGeometry()

    _widget.move(screen_rect.center() - _widget.rect().center())

    _widget.raise_()
    _widget.activateWindow()

    if not app_existed:
        # Run standalone
        app.exec_()
        # sys.exit(app.exec() if hasattr(app, "exec") else app.exec_())


if __name__ == '__main__':
    main()