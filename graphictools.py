# Script responsavel por plotar os graficos no visualizador do software
import numpy as np
import matplotlib.cm as cm

# canvas do matplotlib
import matplotlib as mpl
mpl.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.backends.qt_compat import (
    QtWidgets, __version__,
    _enum,  _getSaveFileName
)
import matplotlib.dates as mdates
import os


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
                self.canvas.figure.savefig(fname, figsize = (14, 9), dpi = 300, bbox_inches="tight")
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Erro ao salvar o arquivo", str(e),
                    _enum("QtWidgets.QMessageBox.StandardButton").Ok,
                    _enum("QtWidgets.QMessageBox.StandardButton").NoButton)


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent = None, width = 16, height = 7, dpi = 100):
        # startup properties
        mpl.rcParams.update({
            'axes.spines.top' : False,
            'axes.spines.right' : False,
            'axes.spines.left' : False,
            'figure.subplot.bottom' : 0.1,
            'figure.subplot.top' : 0.95,
            'axes.grid' : True,
            "axes.grid.axis" : "y",
        })
        
        # iniciando
        self.fig = Figure(figsize = (width, height), dpi = dpi)
        self.axes = self.fig.add_subplot(111)
        self.p = parent
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
        super(MplCanvas, self).__init__(self.fig)

    def updateLegend(self, ncol = 4, size = 10):
        if not isinstance(self.legend, type(None)):
            self.legend.remove()

        handles, IDs = self.axes.get_legend_handles_labels()
        for j in range(len(IDs)):
            IDs[j] = self.alias.get(IDs[j], IDs[j])

        props = dict(
            loc = 8, ncol = ncol, fancybox = True, shadow = False,
            prop = dict(family = "Arial", weight = "bold", size = size)
            )
            
        self.legend = self.fig.legend(handles, IDs, **props)
        self.draw()

    def updateColor(self, id_, color):
        handles, labels = self.axes.get_legend_handles_labels()
        if id_ in labels:
            i = labels.index(id_)
            if isinstance(handles[i], mpl.container.BarContainer):
                for patch in handles[i].patches:
                    patch.set_facecolor(color)
            else:
                handles[i].set_color(color)
        
        # if isinstance(self.p.ds, type(None)):
        #     self.colors['Faixa Limite'] = color
        # else:
        self.colors[id_] = color
        self.draw()

    def reset(self):
        # limpa os elementos do eixo
        self.axes.cla()
        args = ["label", "xlabel", "ylabel"]
        properties = []
        for idx in range(len(args)):
            d = {}
            d[args[idx]] = eval("self.{}".format(args[idx]))
            d['fontsize'] = eval("self.{}_fontsize".format(args[idx]))
            d['fontweight'] = eval("self.{}_fontweight".format(args[idx]))
            properties.append(d)
        
        # adiciona novamente.
        self.axes.set_title(**properties[0])
        self.axes.set_xlabel(**properties[1])
        self.axes.set_ylabel(**properties[2])

    def barPlot(self, ds, resultados):
        # Deduzindo a frequencia do eixo X
        x = ds.index
        x = mdates.date2num(x)
        dx = np.roll(x, 1) - x
        unique, counts = np.unique(dx, return_counts=True)
        freq = np.asarray((unique, counts)).T
        ii = np.where(freq[:, 1] == np.nanmax(freq[:, 1]))[0][0]
        dx = np.abs(freq[ii, 0])
     
        # insere no plot atual
        width = 0.8 * dx
        div = ds.shape[1]
        cmap = cm.get_cmap("jet")
        cores = np.linspace(0, 1, div)
        colunas = ds.get_columns()
        max_ = np.zeros(len(colunas))
        min_ = np.zeros(len(colunas))

        for i, col in enumerate(colunas):
            id_ = ds.ID[col]
            times = mdates.num2date(x + width / div * (i - div // 2))
            y = resultados[col]
            max_[i] = np.nanmax(y, axis = 0)
            min_[i] = np.nanmin(y, axis = 0)
            cor = self.colors.get(id_, cmap(cores[i]))
            self.axes.bar(times, y, width = width/div, label = id_, edgecolor = "none", color = cor)
            self.colors[id_] = cor
            if not id_ in self.alias:
                self.alias[id_] = col
            
        # X ticks
        self.xticks = x
        self.xtick_labels = ds.index
        self.smart_xticks()

        # Y ticks
        max_ = np.nanmax(max_)
        if self.ytick_max < max_:
            self.ytick_max = np.ceil(max_)*1.3
        if np.nanmin(min_) < 0:
            self.ytick_min = np.floor(np.nanmin(min_))*0.8
        self.smart_yticks()

    def linePlot(self, ds, resultados):
        # Insere o Plot atual
        div = ds.shape[1]
        cmap = cm.get_cmap("jet")
        cores = np.linspace(0, 1, div)
        colunas = ds.get_columns()
        max_ = np.zeros(len(colunas))
        min_ = np.zeros(len(colunas))

        for i, col in enumerate(colunas):
            y = resultados[col]
            id_ = ds.ID[col]
            max_[i] = np.nanmax(y, axis = 0)
            min_[i] = np.nanmin(y, axis = 0)
            cor = self.colors.get(id_, cmap(cores[i]))
            self.axes.plot(ds.index, y, label = id_, color = cor, linestyle = "-")
            self.colors[id_] = cor
            if not id_ in self.alias:
                self.alias[id_] = col
            
        # X ticks
        self.xticks = ds.index
        self.xtick_labels = ds.index
        self.smart_xticks()

        # Y ticks
        max_ = np.nanmax(max_)
        if self.ytick_max < max_:
            self.ytick_max = np.ceil(max_)*1.3
        if np.nanmin(min_) < 0:
            self.ytick_min = np.floor(np.nanmin(min_))*1.2
        self.smart_yticks()

    def ultrapassagensPlot(self, ds, resultados):
        # prepara os resultados
        padrao = self.p.GraficoTab.value_limite.value()

        # Extraindo a maxima, segunda maxima e o numero de ultrapassagens.
        maxima = np.full(ds.shape[1], np.nan)
        segunda_maxima = np.full(ds.shape[1], np.nan)
        ultrapassagens = np.zeros(ds.shape[1])
        colunas = ds.get_columns()
        for i, col in enumerate(colunas):
            ordenado = np.sort(resultados[col][~np.isnan(resultados[col])])
            maxima[i] = ordenado[-1]
            segunda_maxima[i] = ordenado[-2]
            ultrapassagens[i] = np.sum(ordenado > padrao, axis = 0)

        # Insere o Plot atual
        x = np.arange(ds.shape[1])
        div = 3
        width = 0.8
        cmap = cm.get_cmap("rainbow")
        cores = np.linspace(0, 1, div)
        labels = ["Máxima", "Segunda Máxima", "Nº de Ultrapassagens"]
        for i, arr in enumerate([maxima, segunda_maxima, ultrapassagens]):
            id_ = labels[i]
            cor = self.colors.get(id_, cmap(cores[i]))
            rect = self.axes.bar(x + width/div*(i - div//2), arr, width/div, label = id_, edgecolor = "none", color = cor)
            self.axes.bar_label(rect, padding=3, fmt = "%.0f", fontname = "Arial", weight = "bold")
            self.colors[id_] = cor
            if not id_ in self.alias:
                self.alias[id_] = labels[i]
            
        # X ticks
        new_labels = ["-".join(string.split('-')[:-1]) for string in colunas]
        self.xticks = x
        self.xtick_labels = new_labels
        self.xtick_min = np.min(x) - 1
        self.xtick_max = np.max(x) + 1
        self.xtick_size = x.shape[0] + 2
        self.axes.set_xticks(x)
        self.axes.set_xticklabels(new_labels)
        self.axes.set_xlim(self.xtick_min, self.xtick_max)
        # self.smart_xticks()

        # Y ticks
        everything = np.stack((maxima, segunda_maxima, ultrapassagens))
        max_ = np.nanmax(everything)
        min_ = np.nanmin(everything)
        if self.ytick_max < max_:
            self.ytick_max = np.ceil(max_)*1.3
        if np.nanmin(min_) < 0:
            self.ytick_min = np.floor(np.nanmin(min_))*0.8
        self.smart_yticks()

    def smart_xticks(self, **kwargs):
        # resgata as variaveis
        rotation = kwargs.get('rotation', self.xtick_rotation)
        range_format = kwargs.get("dateformat", self.xlabel_dateformat)
        date_range = kwargs.get("daterange", self.xlabel_daterange)
        fontsize = kwargs.get("fontsize", self.xticks_fontsize)

        if not isinstance(self.xtick_labels[0], np.datetime64):
            # resgata as variaveis
            min_ = kwargs.get('min_', self.xtick_min)
            max_ = kwargs.get('max_', self.xtick_max)
            size = kwargs.get('size', self.xtick_size)

            # procedimentos
            ticks = np.linspace(min_, max_, size)
            ticks = np.unique(np.ceil(ticks).astype(int))
            self.axes.set_xticks(ticks)
            self.axes.set_xlim(min_, max_)

            # atualiza os valores
            self.xtick_max = np.max(ticks)
            self.xtick_min = np.min(ticks)
            self.xtick_size = ticks.shape[0]

        else:
            # Caso seja um objeto datetime
            strFormat1 = {
                "Dia" : "datetime64[D]",
                "Mês" : "datetime64[M]",
                "Ano" : "datetime64[Y]"
            }
            date_formatter = {
                "datetime64[D]": ("%d/%m/%Y", mdates.DayLocator(interval = date_range)),
                "datetime64[M]" : ("%d/%m/%Y", mdates.MonthLocator(interval = date_range)), 
                "datetime64[Y]" : ("%Y", mdates.YearLocator())
            }

            datetime_str = strFormat1.get(range_format, "datetime64[D]")
            self.axes.xaxis.set_major_formatter(
                mdates.DateFormatter(date_formatter[datetime_str][0])
                )
            self.axes.xaxis.set_major_locator(date_formatter[datetime_str][1])
            self.fig.autofmt_xdate() 

            # atualiza as variavies na classe
            self.xlabel_dateformat = range_format
            self.xlabel_daterange = date_range
            dx = self.xticks[2] - self.xticks[1]
            max_ = np.max(self.xticks) + dx
            min_ = np.min(self.xticks) - dx
            self.axes.set_xlim(min_, max_)

        # Testes para formatacao dos rotulos no eixo X.
        self.axes.tick_params(axis='x', which='major', labelsize=fontsize)

        self.xtick_rotation = rotation
        self.xticks_fontsize = fontsize
        self.draw()

        return None

    def smart_yticks(self, **kwargs):
        # resgata as variaveis
        min_ = kwargs.get('min_', self.ytick_min)
        max_ = kwargs.get('max_', self.ytick_max)
        size = kwargs.get('size', self.ytick_size)
        fontsize = kwargs.get('fontsize', self.yticks_fontsize)

        # procedimentos
        ticks = np.linspace(min_, max_, size)
        ticks = np.unique(np.ceil(ticks).astype(int))
        self.axes.set_yticks(ticks)
        self.axes.set_ylim(min_, max_)
        self.axes.tick_params(axis='y', which='major', labelsize=fontsize)

        # atualiza os valores
        self.ytick_max = np.max(ticks)
        self.ytick_min = np.min(ticks)
        self.ytick_size = ticks.shape[0]
        self.yticks_fontsize = fontsize

        self.draw()
        return None

    def hline_faixa(self, yvalue):
        id_ = 'Faixa Limite'
        left, right = self.axes.get_xlim()
        bottom, top = self.axes.get_ylim()
        color = self.colors.get(id_, (1, 0, 0))
        props = dict(color = color, linestyle = "-", label = id_, linewidth = 4)
        self.axes.hlines(yvalue, xmin = left - 1, xmax = right + 1, **props)
        self.colors[id_] = color
        self.alias[id_] = self.alias.get(id_, "Limite")

        self.axes.set_xlim(left, right)
        self.axes.set_ylim(bottom, top)
        self.draw()


