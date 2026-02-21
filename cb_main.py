# coding: utf-8

import nuke

import cb_widget
from cb_helper import load_groups


def create_node(node_data):
    """
    Create a new node based on the node_data.

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

    node_class = str(node_data.get('node_class'))
    if not [node_class]:
        nuke.message('Something wrong in the database.\n'
                     'Impossible to create the node!')
        return None

    knob_values = str(node_data.get('knob_values', ''))
    open_prop = bool(node_data.get('inpanel', True))

    try:
        nuke.createNode(node_class,
                        knob_values,
                        inpanel=open_prop)

    except RuntimeError as error:
        nuke.message("Unable to create the node!\n {}".format(error))

def main(group):
    saved_data = load_groups()
    group_data = saved_data.get(group)

    if not group_data:
        nuke.message('No data found for this group.')
        return

    cb_widget.main(group_data, create_node)

























