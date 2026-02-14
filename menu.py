import nuke

import cb_info
from cb_menu_builder import build_menu

nuke.tprint('\n\t {} v{} '.format(cb_info.__title__,
                                  cb_info.__version__))

if nuke.GUI:
    build_menu()