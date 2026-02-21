# coding: utf-8

import os
import json


def get_json_file(filename='cb_groups.json'):
    """
    Build the JSON file path based on the installation directory.

    Args:
        filename (str): the name of the JSON file to save.
            cb_groups (default) for the nodes groups,
            cb_settings for the widget settings.

    Returns:
        json_file (str): the JSON file path.

    """
    filename = filename if filename.endswith('.json') else "{}.json".format(filename)
    return os.path.join(os.path.dirname(__file__), filename)

def load_groups(filename='cb_groups'):
    """
    Load the content of the JSON file if it exists.

    Args:
        filename (str): the name of the JSON file to save.
            cb_groups (default) for the nodes groups,
            cb_settings for the widget settings.

    Returns:
        data (dict): the content of the JSON file, or None.
    """
    json_file = get_json_file(filename)
    if os.path.exists(json_file):
        with open(json_file, 'r') as rf:
            return json.load(rf)

    return None

def save_groups(groups, filename='cb_groups'):
    """
    Save the updated dict to the JSON file. Create a new one if it doesn't exist.

    Args:
        groups (dict): a dict separated by Groups, where each group have a list of nodes and settings.
        filename (str): the name of the JSON file to save, default to 'cb_groups.
            cb_groups for the nodes groups,
            cb_settings for the widget settings.
    """
    json_file = get_json_file(filename)

    with open(json_file, 'w') as wf:
        json.dump(groups, wf, indent=4)
