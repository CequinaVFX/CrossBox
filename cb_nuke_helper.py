# coding: utf-8

import nuke

import cb_main
import cb_manager
from cb_helper import load_boxes


"""
Float / Int	        '0.5'
Bool	            'true' / 'false'
Color (RGBA)	    '{r g b a}'
Box	                '{x y r t}'
XY	                '{x y}'

nuke.createNode('Constant', 'color {0.3 0.7 0.5 1}', inpanel=False)
nuke.createNode('Text2', 'box {0 0 width height}', inpanel=True)

"""
#
# def collect_valid_knobs(pref_node):
#
#
#     if nuke.NUKE_VERSION_MAJOR > 13:
#         return [k for k in sorted(pref_node.knobs()) if 'slot' in k.lower()], [k for k in sorted(pref_node.knobs()) if 'choice' in k.lower()]
#
#     else:
#         _classes = [k for k in sorted(pref_node.knobs()) if 'nodecolourclass' in k.lower()]
#         _colours = []
#         if _classes:
#             for index, class_name in enumerate(_classes):
#                 search = class_name.split('ss')[1]
#                 if search:
#                     _colours.append("NodeColour{}Color".format(search)) #  = [k for k in sorted(pref_node.knobs()) if node_color in k.lower()]
#         return _classes, _colours
#
# def get_tile_color(node):
#     pref_node = nuke.toNode('preferences')
#     node_tile_color = '60, 60, 60'
#
#     classes_knobs, _colour_knobs = collect_valid_knobs(pref_node)
#
#     if classes_knobs:
#
#         node_class = node.Class().lower()
#         node_tile_color = node['tile_color'].value()
#
#         if node_tile_color == 0:
#             node_tile_color = None
#
#             for class_slot in classes_knobs:
#                 print(class_slot)
#                 node_class_slot = [i.lower() for i in pref_node[class_slot].value().split() if i.lower() == node_class]
#                 if node_class_slot:
#                     _slot = class_slot.split('ss')
#                     print(_slot)
#                     # class_color= "NodeColour{}Color".format(_slot)
#                     # node_tile_color = pref_node[class_color].value()
#                     # print('found tile color', node_tile_color)
#
#             if node_tile_color == None:
#                 node_tile_color = pref_node['NodeColor'].value()
#                 print('color is NONE', node_tile_color)
#
#     return node_tile_color
#
#
# ki = get_tile_color(nuke.selectedNode())
#
# print()
#
# for k in ki:
#     print(k)
#
#
# # ki = getTileColor(nuke.selectedNodes())

IGNORE = ['xpos', 'ypos', 'selected', 'useLifetime', 'lifetimeStart', 'lifetimeEnd',
          'postage_stamp', 'postage_stamp_frame', 'hide_input', 'cached', 'disabled',
          'dope_sheet', 'bookmark', 'indicators']

def int_to_rgb(tile_color):
    r = (tile_color >> 24) & 0xFF
    g = (tile_color >> 16) & 0xFF
    b = (tile_color >> 8) & 0xFF
    # a = tile_color & 0xFF
    return r, g, b  ## to return normalized > r/255.0, g/255.0, b/255.0, a

def get_user_modified_knobs(node):
    result = []

    for knob in node.knobs().values():
        if any([knob.name() in IGNORE, not knob.visible(), knob.isAnimated(), knob.hasExpression()]):
            # Ignore knobs from the list above, invisible, animated or with expression
            continue

        try:
            if knob.value() != knob.defaultValue():
                result.append('{} {}'.format(knob.name(), knob.value()))
        except:
            pass

    return result

def collect_knob_values(node=None):
    result = get_user_modified_knobs(node)

    return {
        "label": node.Class().lower(),
        "node_class": node.Class(),
        "shortcut": node.Class().lower()[0],
        "knob_values": ' '.join(result),
        "color": int_to_rgb(node['tile_color'].value()),
        "inpanel": True
    }

def get_selected_node():
    nodes = nuke.selectedNodes()
    if len(nodes) == 1:
        return collect_knob_values(nuke.selectedNode())

    elif len(nodes) > 1:
        nuke.message('Select only one node.')
    else:
        nuke.message('Select a node.')

    return None

def add_to_menu(nuke_menu, label, command, shortcut=None, icon=None, add_separator=False):
    """
    Add a new menu commando to the top-level or sub-menu Nuke's Nodes toolbar.

    Args:
        nuke_menu (nuke.MenuBar): Nuke's menu instance
        label (str): display text shown in the menu
        command (str): Python command or callable to execute
        shortcut (str, optional): keyboard shortcut key. Defaults to None
        icon (str, optional): icon path to be shown in the menu. Defaults to None.
        add_separator (bool, optional): If true, add a visual separator line above the new entry. Defaults to False
    """
    if add_separator:
        nuke_menu.addSeparator()

    nuke_menu.addCommand(label, command, shortcut, icon=icon, shortcutContext=2)

def build_menu():
    """
    Build the CrossBox menu, and add each Group as a command.
    If JSON doesn't exist, it will add only the Manager to the menu, where the user can create a new json file.
    """
    boxes = load_boxes()

    if boxes:
        toolbar = nuke.toolbar("Nodes")
        cb_menu = toolbar.addMenu('CrossBox')

        for gr_name, value in boxes.items():
            _settings = value.get('settings')
            _label = _settings.get('label')
            shortcut = _settings.get('shortcut')

            label = "Crossbox [{}]".format(_label.capitalize())
            nuke_command = "cb_main.main('{}')".format(gr_name)
            add_to_menu(cb_menu, label, nuke_command, shortcut)

        add_to_menu(cb_menu, 'Crossbox Manager', 'cb_manager.main()', add_separator=True)

    else:
        # Add only the CrossBox manager in case didn't find the JSON file.
        toolbar = nuke.toolbar("Nodes")
        cb_menu = toolbar.addMenu('CrossBox')
        add_to_menu(cb_menu, 'Crossbox Manager', 'cb_manager.main()', add_separator=True)

def update_menu():
    """
    Updates the CrossBox menu either adding or removing entries.

    """
    boxes = load_boxes()

    if boxes:
        toolbar = nuke.toolbar('Nodes')
        cb_menu = toolbar.findItem('CrossBox')

        for gr_name, value in boxes.items():
            _settings = value.get('settings')
            _label = _settings.get('label')
            shortcut = _settings.get('shortcut')

            label = "Crossbox [{}]".format(_label.capitalize())
            nuke_command = "cb_main.main('{}')".format(gr_name)

            _find = cb_menu.findItem(label)
            if _find:
                cb_menu.removeItem(_find.name())

            add_to_menu(cb_menu, label, nuke_command, shortcut)



"""
https://learn.foundry.com/nuke/developers/140/pythonreference/_autosummary/nuke.MenuBar.html

print()

commands = ['cmd 1', 'cmd B', 'cmd GG']

def add_menu(menu, label, cmd, shortcut=None):
    menu.addCommand(label, nuke_command)

def build_menu():
    toolbar = nuke.toolbar("Nodes")
    m = toolbar.addMenu('CMDs')
    for cmd in commands:
        label = "Command [{}]".format(cmd.capitalize())
        nuke_command = "print({})".format(cmd)
        # m.addCommand(label, nuke_command)
        add_menu(m, label, nuke_command)

    m.addSeparator()
    m.addCommand('Crossbox Manager', 'print("manager")')


def update_menu():
    toolbar = nuke.toolbar('Nodes')
    cmd_menu = toolbar.findItem('CMDs')

    for cmd in commands:
        label = "Command [{}]".format(cmd.capitalize())

        find = cmd_menu.findItem(label)
        if find:
            print(cmd_menu.removeItem(find.name()))
            # cmd = 'print("{}")'.format(label)
            # add_menu(cmd_menu, label, cmd)

update_menu()


"""