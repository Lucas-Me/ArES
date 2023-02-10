'''
CONTEM AS CLASSES RESPONSAVEIS PELA VISUALIZACAO EM GRAFICO NA QUINTA PAGINA DO SOFTWARE
'''

# IMPORT MODULES
import os
import numpy as np

# IMPORT PLOT RELATED MODULES
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.backends.qt_compat import (
    QtWidgets, __version__,
    _enum,  _getSaveFileName
)

# DEFAULT MATPLOTLIB OPTIONS
# ///////////////////////////////////////////////////////////////////////
mpl.use("QtAgg")
mpl.rcParams.update({
	'axes.spines.top' : False,
	'axes.spines.right' : False,
	'axes.spines.left' : False,
	'figure.subplot.bottom' : 0.1,
	'figure.subplot.top' : 0.95,
	'axes.grid' : True,
	"axes.grid.axis" : "y",
})

# CLASSES
# ///////////////////////////////////////////////////////////////////////

class NavigationToolbar(NavigationToolbar2QT):

    def __init__(self, canvas, parent):
        # only display the buttons we need
        NavigationToolbar2QT.toolitems = (
            ('Home', 'Reiniciar visão original', 'home', 'home'),
            ('Back', 'Voltar a operação anterior', 'back', 'back'),
            ('Forward', 'Avançar para a operação seguinte', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Navegue com o clique esquerdo, dê zoom com o direito.', 'move', 'pan'),
            ('Zoom', 'Dê zoom para o retangulo', 'zoom_to_rect', 'zoom'),
            # ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'), (None, None, None, None),
            ('Save', 'Salvar a figura', 'filesave', 'save_figure')
        )
        super().__init__(canvas, parent)

    # sobrescreve a função "save_figure"
    def save_figure(self, *args):
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = sorted(filetypes.items())
        default_filetype = self.canvas.get_default_filetype()

        startpath = os.path.expanduser(mpl.rcParams['savefig.directory'])
        start = os.path.join(startpath, self.canvas.get_default_filename())
        filters = []
        selectedFilter = None
        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter_ = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selectedFilter = filter_
            filters.append(filter_)
        filters = ';;'.join(filters)

        fname, filter_ = _getSaveFileName(
            self.canvas.parent(), "Choose a filename to save to", start,
            filters, selectedFilter)
        if fname:
            # Save dir for next time, unless empty str (i.e., use cwd).
            if startpath != "":
                mpl.rcParams['savefig.directory'] = os.path.dirname(fname)
            try:
                self.canvas.figure.savefig(fname, dpi = 300, bbox_inches="tight")
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Erro ao salvar o arquivo", str(e),
                    _enum("QtWidgets.QMessageBox.StandardButton").Ok,
                    _enum("QtWidgets.QMessageBox.StandardButton").NoButton)


class AbstractCanvas(FigureCanvasQTAgg):

    def __init__(self, width = 16, height = 7, dpi = 100):

        
        # iniciando
        self.fig = Figure(figsize = (width, height), dpi = dpi)
        self.axes = self.fig.add_subplot(111)
		
		# wtf?
        self.colors = {}
        self.alias = {}
        
        # propriedades do grafico
        self.legend = None
        self.label = self.axes.title.get_text()
        self.label_fontsize = self.axes.title.get_fontsize()
        self.label_fontweight = self.axes.title.get_fontweight()

        # Eixo Horizontal
        self.xlabel = self.axes.xaxis.get_label().get_text()
        self.xlabel_fontsize = self.axes.xaxis.get_label().get_fontsize()
        self.xlabel_fontweight = self.axes.xaxis.get_label().get_fontweight()
        self.xticks_fontsize = mpl.rcParams['font.size']
        self.xlabel_dateformat = "Mês"
        self.xlabel_daterange = 1
        #
        self.xticks = self.axes.get_xticks()
        self.xtick_labels = self.axes.get_xticklabels()
        self.xtick_rotation = 0
        #
        self.xtick_min = 0
        self.xtick_max = self.axes.get_xticks().max()
        self.xtick_size = self.xticks.shape[0]

        # Eixo Vertical
        self.ylabel = self.axes.yaxis.get_label().get_text()
        self.ylabel_fontsize = self.axes.yaxis.get_label().get_fontsize()
        self.ylabel_fontweight = self.axes.yaxis.get_label().get_fontweight()
        self.yticks_fontsize = mpl.rcParams['font.size']
        #
        self.ytick_max = self.axes.get_yticks().max()
        self.ytick_min = 0
        self.ytick_size = self.axes.get_yticks().shape[0]

        super(AbstractCanvas, self).__init__(self.fig)
