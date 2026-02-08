# coding: utf-8

import os
import nuke
import json
import crossbox_ui

groups = {
    'transform_group' : {
        'top_group': {
            'tc_button': {
                'label': 'cornerpin',
                'node_class': 'CornerPin2D',
                'shortcut': '',
                'knob_values': '',
                'color': '160, 55, 120'}
        },
        'center_group': {
            'cl_button': {
                'label': 'transform masked',
                'node_class': 'TransformMasked',
                'shortcut': 'r',
                'knob_values': '',
                'color': '160, 55, 120'},
            'cc_button': {
                'label': 'transform',
                'node_class': 'Transform',
                'shortcut': 't',
                'knob_values': '',
                'color': '160, 55, 120'},
            'cr_button': {
                'label': 'tracker',
                'node_class': 'Tracker4',
                'shortcut': 'y',
                'knob_values': '',
                'color': '160, 55, 120'},
        },
        'bottom_group': {
            'bc_button': {
                'label': 'crop',
                'node_class': 'Crop',
                'shortcut': 'g',
                'knob_values': '',
                'color': '160, 55, 120'}
        },
        },
    'filter_group' : {
        'top_group': {
            'tc_button': {
                'label': 'zdefocus',
                'node_class': 'ZDefocus2',
                'shortcut': 'h',
                'knob_values': 'math direct size 20 max_size 100',
                'color': '160, 55, 120'}
        },
        'center_group': {
            'cl_button': {
                'label': 'erode',
                'node_class': 'Dilate',
                'shortcut': 'v',
                'knob_values': 'channels alpha',
                'color': '160, 55, 120'},
            'cc_button': {
                'label': 'blur',
                'node_class': 'Blur',
                'shortcut': 'b',
                'knob_values': 'size 15 channels alpha',
                'color': '160, 55, 120'},
            'cr_button': {
                'label': 'defocus',
                'node_class': 'Defocus',
                'shortcut': 'n',
                'knob_values': '',
                'color': '160, 55, 120'},
        },
        'bottom_group': {
            'bc_button': {
                'label': 'blur rgba',
                'node_class': 'Blur',
                'shortcut': '',
                'knob_values': 'size 250 channels rgba',
                'color': '160, 55, 120'}
        },
        }
}

## JSON functions
def load_groups():
    json_file = get_json_file()
    if json_file:
        with open(json_file, 'r') as rf:
            return json.load(rf)

    return None

def get_json_file():
    _file = get_json_file()
    if os.path.exists(_file): return _file

    return None

def save_groups_to_file(groups):
    pass

## Nuke related functions
def create_node(node_data):
    # Collected data example:
    # 'color': '160, 55, 120',
    # 'node_class': 'Blur',
    # 'shortcut': 'b',
    # 'knob_values': 'size 15 channels alpha',
    # 'label': 'blur'

    node_class = str(node_data['node_class'])
    knob_values = str(node_data['knob_values'])

    if node_class and knob_values:
        new_node = nuke.createNode(node_class,
                                   knob_values,
                                   inpanel=False)

    else:
        new_node = nuke.createNode(node_class,
                                   inpanel=False)

def main(group):
    _groups = ''
    group_data = groups[group]
    if not group_data:
        print('Group not found')
        return

    crossbox_ui.main(group_data, create_node)

























