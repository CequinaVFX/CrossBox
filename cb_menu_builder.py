import nuke

import cb_main
import cb_manager
from cb_helper import load_groups


def add_to_menu(nuke_menu, label, command, shortcut=None, icon=None, add_separator=False):
    """
    Add a new menu commando to the top-level or sub-menu Nuke's Nodes toolbar.

    Args:
        nuke_menu (nuke.MenuBar): Nuke's menu instance
        label (str): display text shown in the menu
        command (str): Python command or callable to execute
        shortcut (str, optional): keyboard shotcut key. Defaults to None
        icon (str, optional): icon path to be shown in the menu. Defaults to None.
        add_separator (bool, optional): If true, add a visual separator line above the new entry. Defaults to False
    """
    if add_separator:
        nuke_menu.addSeparator()

    nuke_menu.addCommand(label, command, shortcut, icon=icon)


def build_menu():
    """
    Build the CrossBox menu, and add each Group as a command.
    If JSON doesn't exist, it will add only the Manager to the menu, where the user can create a new json file.
    """
    groups = load_groups()

    if groups:
        toolbar = nuke.toolbar("Nodes")
        cb_menu = toolbar.addMenu('CrossBox')

        for gr_name, value in groups.items():
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
    groups = load_groups()

    if groups:
        toolbar = nuke.toolbar('Nodes')
        cb_menu = toolbar.findItem('CrossBox')

        for gr_name, value in groups.items():
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