# coding: utf-8

import os
import json


def get_json_file():
    """
    Build the json file path based on the installation directory.

    Returns:
        json_file (str): the json file path.
    """
    return os.path.join(os.path.dirname(__file__), 'cb_groups.json')

def load_groups():
    """
    Load the content of the json file if it exists.
    Returns:
        data (dict): the content of the json file, or None.
    """

    json_file = get_json_file()
    if os.path.exists(json_file):
        with open(json_file, 'r') as rf:
            return json.load(rf)

    return None

def save_groups(groups):
    """
    Save the updated dict to the json file. Create a new one if doesn't exist.
    Args:
        groups (dict): a dict separated by Groups, where each groups has a list of nodes and settings.
    """
    json_file = get_json_file()

    with open(json_file, 'w') as wf:
        json.dump(groups, wf, indent=4)
