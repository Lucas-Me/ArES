'''
CONTEM AS CLASSES RESPONSAVEIS PELA VISUALIZACAO EM GRAFICO.
'''
# IMPORT QT CORE
from qt_core import *

# IMPORT MODULES
import numpy as np
import datetime

# IMPORT CUSTOM MODULES
from backend.plot.collections import CustomLineCollection
import backend.misc.settings as settings

# IMPORT PLOT RELATED MODULES
import matplotlib.dates as mdates
import matplotlib.container as mcontainer
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
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
    'lines.linewidth' : .9,
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
    'font.family' : settings.SETTINGS['figura']['font_family'],
    'font.size' : settings.SETTINGS['figura']['font_size'],
    'axes.prop_cycle' : plt.cycler(color = color_list),

    # legend
    'legend.loc' : 'upper center',
    'legend.frameon' : False,
    'legend.fancybox' : False,
    'legend.shadow' : False,

    # subplot adjust
    'figure.subplot.bottom' : settings.SETTINGS['figura']['bottom'],
    'figure.subplot.left' : settings.SETTINGS['figura']['left'],
    'figure.subplot.right' : settings.SETTINGS['figura']['right'],
    'figure.subplot.top' : settings.SETTINGS['figura']['top']
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
        # /////////////////////////////////////
        self.colors = {} # store colors
        self.labels = {} # store labels
        self.handles = {} # store artists
        self.ylims = {} # stores bottom and top for each artist
        self.xlims = {} # stores left and right for each artist
        self.legend = self.fig.legend([], [])
        self.iter_color = iter(mpl.rcParams['axes.prop_cycle'])

        # annotation 
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="grey"),
                    arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

        # timer
        self.timer = QTimer()
        m = 100
        self.time_count = 0
        self.timer.timeout.connect(lambda: self.updateCount(m))
        self.timer.setInterval(m)
        self.MAX_TIME = 300

        # autoadjust axis options
        self.autoadjust_yaxis = True
        self.autoadjust_xaxis = True

        # /////////////////////////////////////
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
        # /////////////////////////////////////
        super(AbstractCanvas, self).__init__(self.fig)

        # SIGNALS AND SLOTS
        # /////////////////////////////////////
        self.mpl_connect('pick_event', self.on_pick) # legenda
        self.mpl_connect('button_press_event', self.on_click) # titulo dos eixos
        self.mpl_connect("motion_notify_event", self.on_hover) # hover

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
        for patch_, key in zip(self.legend.get_patches(), self.handles.keys()):
            patch_.set_label(key)
            patch_.set_picker(True)

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

        # schedule an update
        self.draw_idle()

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
    
    def plothline(self, y, id_):
        '''Plot a infinite hline with constant y value'''

        # remove if already exists
        self.removePlot(id_)

        # Plot properties
        kwargs = {
            'y' : y,
            'label' : id_,
            'color' : self.colors.get(id_, 'red'),
            'linewidth' : 3,
            'zorder' : 3
        }
        
        # plotting
        lin = self.ax.axhline(**kwargs)
        lin.set_picker(True)

        # storing variables
        self.handles[id_] = lin
        self.labels[id_] = lin.get_label()
        self.colors[id_] = lin.get_color()
        self.ylims[id_] = lin.get_ydata()
        self.xlims[id_] = [np.nan, np.nan]

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
        if id_ in self.xlims:
            del self.xlims[id_]

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

    def autoscaleAxisX(self):
        if not self.autoadjust_xaxis or len(self.xlims) == 0 :
            return None
        
        # estimando o valor maximo e minimo dos objetos no grafico
        values = list(self.xlims.values())
        new_left = np.nanmin(values)
        new_right = np.nanmax(values)

        if new_right == new_left:
            return None

        self.setHorizontalLims(min = new_left, max = new_right)
        self.xaxisAdjusted.emit(new_left, new_right)

    def updateCount(self, msec):
        self.time_count += msec
        if self.time_count > self.MAX_TIME:
            self.timer.stop()
            self.time_count = 0

    def updateAnnotation(self, index : int, line : mlines.Line2D):
        x = line.get_xdata()[index["ind"][0]]
        y = line.get_ydata()[index["ind"][0]]
        self.annot.xy = (x, y)
        self.annot.set_text(f"{line.get_label()[6:]}\n\nY: {y:.2f}\nX: {str(x).replace('T', ' ')}")
        self.annot.get_bbox_patch().set_alpha(0.4)

    def on_pick(self, event : PickEvent):
        dblclick = event.mouseevent.dblclick
        if dblclick and not self.timer.isActive():
            artist = event.artist
            label = artist.get_label()

            self.artistClicked.emit(label)
            self.timer.start()

    def on_click(self, event):
        if event.dblclick and event.inaxes is None and not self.timer.isActive():
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
                self.timer.start()
    
    def on_hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            # itera sobre todos as linhas presentas
            for k, v in self.handles.items():
                if isinstance(v, mlines.Line2D):
                    cont, idx = v.contains(event)
                    if cont and "Faixa Horizontal" not in k:
                        self.annot.set_visible(True)
                        self.updateAnnotation(idx, v)
                        self.draw_idle()
                        return None
                    
            # if visible, then hide.
            if vis:
                self.annot.set_visible(False)
                self.draw_idle()


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
        vmin = self.params['xticks-min']
        vmax = self.params['xticks-max']

        vmin = mdates.num2date(vmin)
        vmax = mdates.num2date(vmax)

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
            'color' : self.colors.get(id_, next(self.iter_color)['color']),
            'zorder' : 2
        }

        # ploting
        hl, = self.ax.plot(dates, values, **kwargs)
        hl.set_picker(True)

        # storing artist, color and labels
        self.handles[id_] = hl
        self.colors[id_] = hl.get_color()
        self.labels[id_] = self.labels.get(id_, series.metadata['alias'])
        self.ylims[id_] = (np.nanmin(values), np.nanmax(values))
        #
        min_date = mdates.date2num(dates.min().item())
        max_date = mdates.date2num(dates.max().item())
        self.xlims[id_] = (min_date, max_date)

        # scaling axis
        self.autoscaleAxisX()
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

        # scaling X axis
        t_final = mdates.date2num(series_list[0].getDates()[-1])
        xmin = t0 - delta_t / 2
        xmax = t_final + delta_t /2

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
                'color' : self.colors.get(id_, next(self.iter_color)['color']),
                'width' : width,
                'zorder' : 1
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
            self.ylims[id_] = (0, np.nanmax(values))
            self.xlims[id_] = (xmin, xmax)
        
        # scaling axis
        self.autoscaleAxisX()
        self.autoscaleAxisY()

        # updating legend
        self.updateLegend()


class OverpassingCanvas(AbstractCanvas):

    def __int__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

        # Properties
        self.values_series = {} # necessary in order to update the count (?)
        self.count = 0 # don't know
        
        # containers
        self.handles['overpassing'] = mcontainer.BarContainer(orientation='Vertical')
        self.handles['first_maximum'] = mcontainer.BarContainer(orientation='Vertical')
        self.handles['second_maximum'] = mcontainer.BarContainer(orientation='Vertical')

        # color for each container
        self.colors['overpassing'] = '#49111C'
        self.colors['first_maximum'] = '#5E503F'
        self.colors['second_maximum'] = '#A9927D'

        # label for each container
        self.labels['overpassing'] = 'Ultrapassagens'
        self.labels['first_maximum'] = 'Máxima'
        self.labels['second_maximum'] = 'Segunda Máxima'
    
        # SETTINGS
        self.plothline(10, id_ = "Limite")

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

        # preparing maximum values
        max_y = [self.params['yticks-max'], np.nanmax(values)]

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
            min = 0
        )
        
        # updating legend
        self.updateLegend()

        # draw
        self.draw()