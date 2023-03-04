'''
CONTEM AS CLASSES RESPONSAVEIS PELA VISUALIZACAO EM GRAFICO.
'''
# IMPORT QT CORE
from qt_core import *

# IMPORT MODULES
import numpy as np

# IMPORT CUSTOM MODULES
from backend.plot.collections import CustomLineCollection
import backend.misc.settings as settings

# IMPORT PLOT RELATED MODULES
import matplotlib.dates as mdates
import matplotlib.container as mcontainer
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import PickEvent
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

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

default_color = 'black'
mpl.rcParams.update({
    'axes.axisbelow': False,
    'axes.edgecolor': 'gray',
    'axes.facecolor': 'None',
    'axes.grid': True,
	"axes.grid.axis" : "y",
    'grid.color' : 'silver',
    'axes.labelcolor': default_color,
    'axes.labelpad' : 8, 
    'axes.titlepad' : 12,
    # 'axes.spines.right': False,
    # 'axes.spines.left': False,
    # 'axes.spines.top': True,
    'figure.facecolor': 'white',
    'lines.solid_capstyle': 'round',
    'lines.linewidth' : .5,
    'patch.edgecolor': 'none',
    'patch.force_edgecolor': False,
    'text.color': default_color,
    'xtick.bottom': True,
    'xtick.color': default_color,
    'xtick.direction': 'out',
    'xtick.top': False,
    'ytick.color': default_color,
    'ytick.direction': 'out',
    'ytick.left': False,
    'ytick.right': False,
    'font.family' : 'Calibri',
    'font.size' : 15,
    'axes.prop_cycle' : plt.cycler(color = color_list),

    # legend
    'legend.loc' : 'upper center',
    'legend.frameon' : False,
    'legend.fancybox' : False,
    'legend.shadow' : False,

    # subplot adjust
    'figure.subplot.bottom' : 0.1,
    'figure.subplot.left' : 0.1,
    'figure.subplot.right' : 0.9,
    'figure.subplot.top' : 0.9
 })

# CLASSES
# ///////////////////////////////////////////////////////////////////////

class AbstractCanvas(FigureCanvasQTAgg):
    
    artistClicked = Signal(str)
    valueChanged = Signal(tuple)
    titleClicked = Signal(int)
    xaxisAdjusted = Signal(object, object)
    yaxisAdjusted = Signal(float, float)
    def __init__(self, width = 16, height = 7, dpi = 100):

        # iniciando
        self.fig = Figure(figsize = (width, height), dpi = dpi)
        self.ax = self.fig.add_subplot(111)
		
		# CUSTOM PROPERTIES
        self.colors = {} # store colors
        self.labels = {} # store labels
        self.handles = {} # store artists
        self.ylims = {} # stores bottom and top for each artist
        self.legend = self.fig.legend([], [])

        # autoadjust axis options
        self.autoadjust_yaxis = True
        self.autoadjust_xaxis = True
    
        # SET LOCATOR AT Y AXIS
        self.ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins = self.ax.get_yticks().shape[0]))

        # Plota linha horizontal em y = 0
        self.hline = self.ax.axhline(y = 0, color = 'k', linewidth = 3)

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
            'yticks-min' : self.ax.get_ylim()[0],
            'yticks-max' : self.ax.get_ylim()[1],
            'yticks-size' : self.ax.get_yticks().shape[0],
            'yticks-fontsize' : mpl.rcParams['font.size'],
            'yticks-fontweight' : 10,
            'yticks-rotation' : 0,
            
            # Rótulos do eixo X
            'xticks-min' : self.ax.get_xlim()[0],
            'xticks-max' : self.ax.get_xlim()[1],
            'xticks-rotation' : self.ax.get_xticklabels()[0].get_rotation(),
            'xticks-fontsize' : mpl.rcParams['font.size'],
            'xticks-fontweight' : 10,

            #legenda
            'legend-ncol' : 3,
            'legend-fontsize': mpl.rcParams['font.size'],
            'legend-loc' : mpl.rcParams['legend.loc']
        }

        # CONSTRUCTOR
        super(AbstractCanvas, self).__init__(self.fig)

        # SIGNALS AND SLOTS
        self.mpl_connect('pick_event', self.on_pick)
        self.mpl_connect('button_press_event', self.on_click)

    def getSettings(self):
        return self.params

    def getThreshold(self, series : object):
        methods = series.metadata['methods']
        threshold = 0
        if len(methods) > 0:
            last_method = methods[-1][1]
            threshold = settings.SETTINGS['representatividade'].get(
                last_method, settings.SETTINGS['representatividade']['Horária']
            )
        
        return threshold

    def updateLegend(self, **kwargs):
        args = dict(
            ncol = kwargs.pop('ncol', self.params['legend-ncol']),
            loc = kwargs.pop('loc', self.params['legend-loc']),
            prop = {'size' : kwargs.pop('fontsize', self.params['legend-fontsize'])}
        )

        # remove old legeend
        self.legend.remove()
        
        # manuallly produces the artist for the legend
        n = len(self.handles)
        handles = [None] * n
        labels = [''] * n
        for i, k in enumerate(self.handles.keys()):
            labels[i] = self.labels[k]
            handles[i] = mpatches.Rectangle([0,0], 0, 0, facecolor = self.colors[k], edgecolor = 'none')

        # creating new legend
        self.legend = self.fig.legend(handles, labels, **args)

        # save options
        self.params['legend-ncol'] = args['ncol']
        self.params['legend-fontsize'] = args['prop']['size']

    def updateColor(self, artist_id, color):
        '''Updates the color of a given artist'''
        artist = self.handles[artist_id]
        if isinstance(artist, mpl.container.BarContainer):
            for patch in artist.patches:
                patch.set_facecolor(color)
        else:
            artist.set_color(color)

        # update color propertie
        self.colors[artist_id] = color

    def resetChart(self):
        # limpa os elementos do eixo
        items = list(self.handles.items())
        for name, artist in items:
            if 'Faixa Horizontal' in name:
                continue

            # deleting artist
            artist.remove()

            # deleting private properties
            del self.handles[name]
            del self.ylims[name]
        
        # Rotulos do eixo Y
        self.autoscaleAxisY()

        # legenda
        self.updateLegend()

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

        # draw
        self.draw()

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

        # draw
        self.draw()

    def setTickParams(self, axis = 'y', **kwargs):
        kwargs = {
            'labelsize' : kwargs.pop('fontsize', self.params[f'{axis}ticks-fontsize']),
            'labelrotation' : kwargs.pop('rotation', self.params[f'{axis}ticks-rotation']),
        }
        
        # changing fontsize or rotation
        self.ax.tick_params(axis=axis, which='major', **kwargs)

        # updating private variables
        self.params[f'{axis}ticks-fontsize'] = kwargs['labelsize']
        self.params[f'{axis}ticks-rotation'] = kwargs['labelrotation']


    def setVerticalTicks(self, **kwargs):
        '''
        Rótulos do eixo Vertical.
        '''
        min_y = kwargs.pop('min', self.params['yticks-min'])
        max_y = kwargs.pop('max', self.params['yticks-max'])
        size = kwargs.pop('size', self.params['yticks-size'])
        
        # update axis ticks
        self.ax.yaxis.get_major_locator().set_params(nbins = size)
        
        # updating limits
        self.ax.set_ylim(min_y, max_y)

        # update private params
        self.params['yticks-min'] = min_y
        self.params['yticks-max'] = max_y
        self.params['yticks-size'] = size
    
    def plothline(self, y, id_ = 'Faixa Horizontal'):
        '''Plot a infinite hline with constant y value'''

        # remove if already exists
        self.removePlot(id_)

        # Plot properties
        kwargs = {
            'y' : y,
            'label' : id_,
            'color' : self.colors.get(id_, 'red'),
            'linewidth' : 3
        }
        
        # plotting
        lin = self.ax.axhline(**kwargs)
        lin.set_picker(True)

        # storing variables
        self.handles[id_] = lin
        self.labels[id_] = lin.get_label()
        self.colors[id_] = lin.get_color()
        self.ylims[id_] = lin.get_ydata()

        # update legend
        self.updateLegend()
        self.autoscaleAxisY()

        # draw
        self.draw()

    def removePlot(self, id_):
        if id_ not in self.handles:
            return None
        
        # deleting artist
        self.handles[id_].remove()

        # deleting private properties
        del self.handles[id_]
        del self.ylims[id_]

        # update plot
        self.updateLegend()

    def setHorizontalLims(self, **kwargs):
        vmin = kwargs.pop('min', self.params['xticks-min'])
        vmax = kwargs.pop('max', self.params['xticks-max'])

        # updating locator and fomatter
        self.ax.set_xlim(vmin, vmax)

        # update private params
        self.params['xticks-min'] = vmin
        self.params['xticks-max'] = vmax

    def autoscaleAxisY(self):
        if not self.autoadjust_yaxis or len(self.ylims) == 0 :
            return None
        
        # estimando o valor maximo e minimo dos objetos no grafico
        values = list(self.ylims.values())
        new_bottom = np.nanmin(values)
        new_top = np.nanmax(values)

        if new_top == new_bottom:
            new_top += 10

        self.setVerticalTicks(min = new_bottom, max = new_top)
        self.yaxisAdjusted.emit(new_bottom, new_top)

    def autoscaleAxisX(self, vmin, vmax):
        if self.autoadjust_xaxis:
            if isinstance(vmin, float):
                vmin = mdates.num2date(vmin)
                vmax = mdates.num2date(vmax)
            
            self.setHorizontalLims(min = vmin, max = vmax)

            # emit signal
            self.xaxisAdjusted.emit(vmin, vmax)

    def on_pick(self, event : PickEvent):
        dblclick = event.mouseevent.dblclick
        if dblclick:
            artist = event.artist
            label = artist.get_label()

            self.artistClicked.emit(label)

    def on_click(self, event):
        if event.dblclick and event.inaxes is None:
            # get mouse properties
            width, height = self.get_width_height()
            x = event.x / width
            y = event.y / height

            # get figure properties
            left = self.fig.subplotpars.left
            right = self.fig.subplotpars.right
            top = self.fig.subplotpars.top
            bottom = self.fig.subplotpars.bottom
            
            # get position of click event
            is_outside_lims  = (x < left, x > right, y < bottom, y > top)
            is_valid = sum(is_outside_lims) == 1
            if is_valid:
                self.titleClicked.emit(is_outside_lims.index(True))
    

class TimeSeriesCanvas(AbstractCanvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # SETTING UP HORIZONTAL AXIS
        self.ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 2))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        
        # PROPERTIES
        self.nbars = 0

        # Propriedades do grafico
        self.params.update({
            # Rotulos do eixo X
            'xticks-min' : self.ax.get_xlim()[0],
            'xticks-max' : self.ax.get_xlim()[1],
            'xticks-locator': self.ax.xaxis.get_major_locator(),
            'xticks-formatter' : self.ax.xaxis.get_major_formatter(),
        })
        
    def getXLims(self):
        vmin = mdates.num2date(self.params['xticks-min'])
        vmax = mdates.num2date(self.params['xticks-max'])

        return (vmin, vmax)

    def setHorizontalTicks(self, **kwargs):
        locator = kwargs.pop('locator', self.params['xticks-locator'])
        formatter = kwargs.pop('formatter', self.params['xticks-formatter'])

        # updating locator and fomatter
        self.ax.xaxis.set_major_locator(locator)
        self.ax.xaxis.set_major_formatter(formatter)

        # update private params
        self.params['xticks-locator'] = locator
        self.params['xticks-formatter'] = formatter

    def resetChart(self):
        super().resetChart()

        # rotulos do eixo X
        self.setHorizontalTicks()
    
    def plot(self, series : object, threshold = 0):
        # getting threshold
        threshold = self.getThreshold(series)

        # getting properties
        values = series.maskByThreshold(threshold) # mascara por quantitativo de dados validos
        dates = series.getDates()

        # object metadata
        id_ = series.metadata['signature']

        # Plot properties
        kwargs = {
            'label' : id_,
            'color' : self.colors.get(id_, None)
        }

        # ploting
        hl, = self.ax.plot(dates, values, **kwargs)
        hl.set_picker(True)

        # storing artist, color and labels
        self.handles[id_] = hl
        self.colors[id_] = hl.get_color()
        self.labels[id_] = self.labels.get(id_, series.metadata['alias'])
        self.ylims[id_] = (np.nanmin(values), np.nanmax(values))

        # scaling axis
        self.autoscaleAxisX(dates.min(), dates.max())
        self.autoscaleAxisY()

        # updating legend
        self.updateLegend()

    def getLineCollection(self, x, y, width, bottom = 0, **kwargs) -> CustomLineCollection:
        '''Collection of vetical lines to replace bars'''
        # sets of y to plot versus vs. x
        ys = np.column_stack([np.full(x.shape, bottom), y])
        xs = np.column_stack([x, x])
        segs = [np.column_stack([xs[i], ys[i]]) for i in range(y.shape[0])]

        line_segments = CustomLineCollection(segs,
                               linewidths=width,
                               linestyles='solid',
                               ax = self.ax, **kwargs)
        
        return line_segments

    def barPlot(self, series_list : list[object]):
        n = len(series_list)

        # largura de cada barra sera definida a partir da menor frequencia dentre os dados
        frequencies = np.fromiter(map(lambda x: x.metadata['frequency'].astype('timedelta64[m]'), series_list), dtype = 'timedelta64[m]')
        freq = np.min(frequencies)
        ref_time = series_list[0].getDates()[0]

        # total width
        total_width = 0.8
        t1 = ref_time.astype('datetime64[m]') + freq
        t1 = mdates.date2num(t1)
        t0 = mdates.date2num(ref_time)
        delta_t = (t1 - t0) * total_width
        width = delta_t / n
        
        # preparing maximum and minimum values
        max_y = [1] * n + [self.params['yticks-max']]
        min_y = [0] * n + [self.params['yticks-min']]

        # loop through each series
        for i in range(n):
            # getting series
            series = series_list[i]

            # remove if already in plot
            self.removePlot(series.metadata['signature'])

            # getting properties
            threshold = self.getThreshold(series)
            values = series.maskByThreshold(threshold)  # mascara por quantitativo de dados validos
            dates = series.getDates()

            # maximum and minimum
            max_y[i] = np.nanmax(values)
            min_y[i] = np.nanmin(values)

            # transform
            dates_num = mdates.date2num(dates)
            
            # getting position of left corner
            offset = width * (2 * i - n + 1) / 2 

            # object metadata
            id_ = series.metadata['signature']

            # Plot properties
            kwargs = {
                'color' : self.colors.get(id_, None),
                'width' : width
            }

            # LINE COLLECTION
            lc = self.getLineCollection(dates_num + offset, values, **kwargs)
            self.ax.add_collection(lc)

            # set picker
            lc.set_label(id_)
            lc.set_picker(True)

            # storing artist, color and labels
            self.handles[id_] = lc
            self.colors[id_] = lc.get_color()[0]
            self.labels[id_] = self.labels.get(id_, series.metadata['alias'])
            self.ylims[id_] = (np.nanmin(values), np.nanmax(values))

        # scaling X axis
        t_final = mdates.date2num(series_list[0].getDates()[-1])
        xmin = t0 - delta_t / 2
        xmax = t_final + delta_t /2
        self.autoscaleAxisX(xmin, xmax)
        
        # scaling Y axis
        self.autoscaleAxisY()

        # updating legend
        self.updateLegend()


class OverpassingCanvas(AbstractCanvas):

    def __int__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

        # Properties
        self.hline_faixa = self.plothline(0)
        self.values_series = {} # necessary in order to update the count
        self.count = 0      
        
        # containers
        self.handles['overpassing'] = mcontainer.BarContainer(orientation='Vertical')
        self.handles['first_maximum'] = mcontainer.BarContainer(orientation='Vertical')
        self.handles['second_maximum'] = mcontainer.BarContainer(orientation='Vertical')

    def resetChart(self):
        super().resetChart()

        # resetting variables
        self.hline_faixa = self.plothline(0)
        self.values_series.clear()
        self.count = 0
        
        # containers
        self.handles['overpassing'] = mcontainer.BarContainer(orientation='Vertical')
        self.handles['first_maximum'] = mcontainer.BarContainer(orientation='Vertical')
        self.handles['second_maximum'] = mcontainer.BarContainer(orientation='Vertical')


    def barPlot(self, series: object):
        # largura de cada barra
        total_width = 0.8
        
        # getting properties
        values = series.getValues()

        sorted_array = values[np.argsort(values)]
        # preparing maximum and minimum values
        max_y = [self.params['yticks-max'], np.nanmax(values)]
        min_y = [self.params['yticks-min'], np.nanmin(values)]

        # bar container elements
        max_value = sorted_array[-1]
        second_max = sorted_array[-2]
        overpasses = np.count_nonzero(values > self.handles['Faixa Horizontal'].get_ydata()[0])
        new_elements = [overpasses, max_value, second_max]

        # bar containers
        bar_containers = ['overpassing', 'first_maximum', 'second_maximum']
        n = 3 

        # loop through each series
        for i in range(n):

            # getting position of left corner
            offset = total_width * (2 * i - n) / (2 * n)

            # getting old rectangles
            rectangles = self.handles[bar_containers[i]].get_children()
            num_r = len(rectangles)

            # Plot properties
            id_ = series.metadata['signature']
            kwargs = {
                'xy' : [num_r + offset, 0],
                'height' : new_elements[i],
                'width' : total_width / n
            }
            
            # creating new rect
            this_rect = mpatches.Rectangle(**kwargs)
            new_rectangles = rectangles + [this_rect]

            # create new bar container
            bc = mcontainer.BarContainer(
                patches = new_rectangles,

            )

            # set picker
            for artist in bc.get_children():
                artist.set_picker(True)
                artist.set_label(id_)
                artist.set_facecolor(self.colors.get(bar_containers[i], None))
                artist.set_edgecolor('none')

            # storing labels and values]
            self.handles[bar_containers[i]] = bc
            self.values_series[id_] = values
            self.labels[id_] = self.labels.get(id_, series.metadata['alias'])
            self.colors[bar_containers[i]] = artist.get_facecolor()
            
            # removing old artists
            self.removePlot(bar_containers[i])

            # adding new artist
            self.ax.add_container(bc)

        # adjusting axis
        self.setVerticalTicks(
            max = np.nanmax(max_y),
            min = np.nanmin(min_y)
        )
        
        # updating legend
        self.updateLegend()

        # draw
        self.draw()