import nuke
import package
import crossbox

nuke.tprint('\n\t {} v{} '.format(package.__title__, package.__version__))

# if nuke.GUI:
toolbar = nuke.toolbar("Nodes")
m = toolbar.addMenu('CrossBox')
m.addCommand('CrossBox [Blur]', 'crossbox.main("filter_group")', 'b')
m.addCommand('CrossBox [Transform]', 'crossbox.main("transform_group")', 't')
