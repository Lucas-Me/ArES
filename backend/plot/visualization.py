'''
CONTEM AS CLASSES RESPONSAVEIS PELA VISUALIZACAO EM GRAFICO NA QUINTA PAGINA DO SOFTWARE
'''

# IMPORT MODULES
import os
import numpy as np
import datetime

# IMPORT PLOT RELATED MODULES
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.backends.qt_compat import (
    QtWidgets, __version__,
    _enum,  _getSaveFileName
)

# DEFAULT MATPLOTLIB OPTIONS
# ///////////////////////////////////////////////////////////////////////

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'

color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]

# mpl.rcParams.update({
# 	'axes.spines.top' : False,
# 	'axes.spines.right' : False,
# 	'figure.subplot.bottom' : 0.1,
# 	'figure.subplot.top' : 0.95,
# 	'axes.grid' : True,
# 	"axes.grid.axis" : "y",
# 	'axes.prop_cycle' : plt.cycler(color = color_list)
# })
mpl.rcParams.update({'axes.axisbelow': False,
 'axes.edgecolor': 'gray',
 'axes.facecolor': 'None',
 'axes.grid': False,
 'axes.labelcolor': 'dimgray',
 'axes.spines.right': False,
 'axes.spines.top': False,
 'figure.facecolor': 'white',
 'lines.solid_capstyle': 'round',
 'patch.edgecolor': 'w',
 'patch.force_edgecolor': True,
 'text.color': 'dimgray',
 'xtick.bottom': False,
 'xtick.color': 'dimgray',
 'xtick.direction': 'out',
 'xtick.top': False,
 'ytick.color': 'dimgray',
 'ytick.direction': 'out',
 'ytick.left': False,
 'ytick.right': False,
 'font.family' : 'Microsoft New Tai Lue'
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
        self.ax = self.fig.add_subplot(111)
		
		# wtf?
        self.colors = {}
        self.alias = {}
        self.legend = None
        
        # PROPRIEDADES DO GRAFICO
        self.params = {
            # Titulo
            'title-label' : self.ax.title.get_text(),
            'title-fontsize' : self.ax.title.get_fontsize(),
            'title-fontweight' : self.ax.title.get_fontweight(),
            
            # Eixo horizontal
            'xaxis-label' : self.ax.xaxis.get_label().get_text(),
            'xaxis-fontsize' : self.ax.xaxis.get_label().get_fontsize(),
            'xaxis-fontweight' : self.ax.xaxis.get_label().get_fontweight(),

            # Eixo vertical
            'yaxis-label' : self.ax.yaxis.get_label().get_text(),
            'yaxis-fontsize' : self.ax.yaxis.get_label().get_fontsize(),
            'yaxis-fontweight' : self.ax.yaxis.get_label().get_fontweight(),

            # Rotulos do eixo Y
            'yticks' : self.ax.get_yticks(),
            'yticks-fontsize' : 12,
            'yticks-fontweight' : 10
        }

        # CONSTRUCTOR
        super(AbstractCanvas, self).__init__(self.fig)

    def setTitle(self, **kwargs):
        kwargs = dict(
            label = kwargs.pop('label', self.params['title-label']),
            fontsize = kwargs.pop('fontsize', self.params['title-fontsize']),
            fontweight = kwargs.pop('fontweight', self.params['title-fontweight'])
        )

        # update title on chart
        self.ax.set_title(**kwargs)

        # update private params
        self.params['title-label'] = kwargs['label']
        self.params['title-fontsize'] = kwargs['fontsize']
        self.params['title-fontweight'] = kwargs['fontweight']

    def setLabel(self, axis = 'x', **kwargs):
        kwargs = {
            f'{axis}label' : kwargs.pop('label', self.params[f'{axis}axis-label']),
            'fontsize' : kwargs.pop('fontsize', self.params[f'{axis}axis-fontsize']),
            'fontweight' : kwargs.pop('fontweight', self.params[f'{axis}axis-fontweight'])
        }

        # update axis label
        if axis == 'x':
            self.ax.set_xlabel(**kwargs)

        else:
            self.ax.set_ylabel(**kwargs)

        # update private params
        self.params[f'{axis}axis-label'] = kwargs[f'{axis}label']
        self.params[f'{axis}axis-fontsize'] = kwargs['fontsize']
        self.params[f'{axis}axis-fontweight'] = kwargs['fontweight']

    def setVerticalTicks(self, **kwargs):
        '''
        Rótulos do eixo Vertical.
        '''
        ticks = kwargs.pop('ticks', self.params['yticks'])
        kwargs = {
            'fontsize' : kwargs.pop('fontsize', self.params['yticks-fontsize']),
            'fontweight' : kwargs.pop('fontweight', self.params['yticks-fontweight'])
        }
        
        # update axis ticks
        self.ax.set_yticks(ticks, **kwargs)

        # update private params
        self.params['yticks'] = ticks
        self.params['yticks-fontsize'] = kwargs['fontsize']
        self.params['yticks-fontweight'] = kwargs['fontweight']


class TimeSeriesCanvas(AbstractCanvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # SETTING UP HORIZONTAL AXIS
        self.ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 2))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

        year = datetime.datetime.now().year
        self.ax.set_xlim(datetime.date(year, 1, 1), datetime.date(year, 12, 31))
        
        # Propriedades do grafico
        self.params.update({
            # Rotulos do eixo X
            'xticks-min' : self.ax.get_xlim()[0],
            'xticks-max' : self.ax.get_xlim()[1],
            'xticks-locator': self.ax.xaxis.get_major_locator(),
            'xticks-formatter' : self.ax.xaxis.get_major_formatter(),
            'xticks-rotation' : 0,
            'xticks-fontsize' : 12,
            'xticks-fontweight' : 10
        })

    def setHorizontalLabels(self, **kwargs):
        rotation = kwargs.pop('rotation', self.params['xticks-rotation'])
        fontsize = kwargs.pop('fontsize', self.params['xticks-fontsize'])
        fontweight = kwargs.pop('fontweight', self.params['xticks-fontweight'])

        # label properties
        for label in self.ax.get_xticklabels(which='major'):
            label.set(rotation=rotation, fontsize = fontsize, fontweight = fontweight)

        # update private params
        self.params['xticks-rotation'] = rotation
        self.params['xticks-fontsize'] = fontsize
        self.params['xticks-fontweight'] = fontweight
        
    def setHorizontalTicks(self, **kwargs):
        locator = kwargs.pop('locator', self.params['xticks-locator'])
        formatter = kwargs.pop('formatter', self.params['xticks-formatter'])

        # updating locator and fomatter
        self.ax.xaxis.set_major_locator(locator)
        self.ax.xaxis.set_major_formatter(formatter)

        # update private params
        self.params['xticks-locator'] = locator
        self.params['xticks-formatter'] = formatter

