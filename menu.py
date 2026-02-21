import nuke

import cb_main
import cb_info
import cb_manager
from cb_nuke_helper import build_menu


nuke.tprint('\n\t {} v{} '.format(cb_info.__title__,
                                  cb_info.__version__))

if nuke.GUI:
    build_menu()
