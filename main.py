import ctypes
import sys
import utilitarios
import gc
import graphictools
import os
import pathlib
import data_management
import numpy as np
import matplotlib as mpl
from PySide6.QtWidgets import (QTreeWidgetItem, QGridLayout, QApplication,
QFileDialog, QMainWindow, QTreeWidget, QHBoxLayout, QWidget, QPushButton,
QLabel, QDateEdit, QVBoxLayout, QComboBox, QLineEdit, QSpinBox, QWidget,
QTabWidget, QGroupBox, QTableWidget, QTableWidgetItem, QColorDialog,
QCheckBox, QHeaderView, QDialog, QMessageBox)
from PySide6.QtCore import QDate, Qt, Slot
from PySide6.QtGui import QColor, QAction, QIcon
from PySide6.QtGui import QFontDatabase


class Tabela(QTreeWidget):

    def __init__(self, parent = None):
        super().__init__()
        self.setHeaderLabels(["Estações de monitoramento"])
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.header().resizeSections()
        self.parentWidget = parent
        self.setColumnCount(1)
        self.itemChanged.connect(self.update_selection)
        self.items = []

    def update(self):
        # Atualiza a tabela sempre que um item e excluido ou adicionado
        self.clear()
        items = []
        for i in range(len(self.parentWidget.arquivos)):
            entity = self.parentWidget.arquivos[i]
            ini = entity.ini.item().strftime("%d/%m/%Y")
            fim = entity.fim.item().strftime("%d/%m/%Y")
            parent = QTreeWidgetItem(self)
            text = f'{entity.tipo} - {entity.nome:40}  {ini:10} a {fim:10}'
            parent.setText(0, text)
            for j in range(len(entity.vars)):
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, entity.vars[j])
                child.setData(1, 0, i)
                child.setData(2, 0, j)
                check_state = Qt.Checked if entity.vars_selected[j] else Qt.Unchecked
                child.setCheckState(0, check_state)

            items.append(parent)
        self.items = items

    def update_selection(self, item, column):

        # verifica se a coluna acionada é a zero
        if column == 0:    
            entity_idx = item.data(1, 0)
            var_idx = item.data(2, 0)

            # verifica se os indices sao objetos None
            if entity_idx is None or var_idx is None:
                return None

            # continua o procedimento
            state = 0
            if item.checkState(column) == Qt.Checked:
                state = 1

            self.parentWidget.arquivos[entity_idx].vars_selected[var_idx] = state

        return None


class TabelaEixos(QTreeWidget):

    def __init__(self, parentWidget = None):
        super().__init__()
        self.parentWidget = parentWidget
        self.setColumnCount(2)
        self.setHeaderLabels(["Propriedades", "Valor"])
        self.header().setSectionResizeMode(QHeaderView.Stretch)
        self.header().resizeSections()

        # variaveis
        self.items_timeseries = {
            "Eixo Horizontal" : [
                "Intervalo",
                "Unidade",
                "Rotação (°)",
                "Tamanho da fonte"],
            "Eixo Vertical" : ["Número de rótulos", "Valor máximo",
                                "Valor mínimo", "Tamanho da fonte"]
        }
        self.items_scatterplot = {
            'Eixo Horizontal' : [
                'Número de rótulos',
                'Valor máximo',
                'Valor mínimo',
                "Tamanho da fonte"
            ],
            'Eixo Vertical' : [
                'Número de Rótulos',
                'Valor Máximo',
                'Valor Mínimo',
                "Tamanho da fonte",
            ]
        }
        self.active_scatter = 0

        # Widgets
        self.intervalo = QSpinBox()
        self.unidade = QComboBox()
        self.rotation_x = QSpinBox()
        self.size_y = QSpinBox()
        self.fontsize_x = QSpinBox()
        self.fontsize_y = QSpinBox()
        self.max_y = QSpinBox()
        self.min_y = QSpinBox()
        self.size_x = QSpinBox()
        self.max_x = QSpinBox()
        self.min_x = QSpinBox()
        
        # widgets list
        self.widgets = [
            {
                'Eixo Horizontal': [self.intervalo, self.unidade,
                                    self.rotation_x, self.fontsize_x],
                'Eixo Vertical' : [self.size_y, self.max_y,
                                    self.min_y, self.fontsize_y]
            },
            {
                'Eixo Horizontal': [self.size_x, self.max_x,
                                    self.min_x, self.fontsize_x],
                'Eixo Vertical' : [self.size_y, self.max_y,
                                    self.min_y, self.fontsize_y] 
                }
        ]

        # configurando widgets
        self.intervalo.setRange(1, 30)
        self.unidade.addItems(['Dia', 'Mês', 'Ano'])
        self.unidade.setCurrentIndex(1)
        self.size_x.setMinimum(1)
        self.size_y.setMinimum(2)
        self.max_y.setRange(-10000, 10000)
        self.fontsize_x.setRange(1, 30)
        self.fontsize_y.setRange(1, 30)
        self.rotation_x.setRange(0, 180)
        mplcanvas = self.parentWidget.canvas
        self.size_x.setMaximum(mplcanvas.xticks.shape[0])
        self.size_x.setValue(mplcanvas.xtick_size)
        self.size_y.setValue(mplcanvas.ytick_size)
        self.max_y.setValue(mplcanvas.ytick_max)
        self.min_y.setValue(mplcanvas.ytick_min)
        self.max_x.setValue(mplcanvas.xtick_max)
        self.min_x.setValue(mplcanvas.xtick_min)
        self.fontsize_x.setValue(mplcanvas.xticks_fontsize)
        self.fontsize_y.setValue(mplcanvas.yticks_fontsize)
    
        # procedimentos
        self.run()
    
        # Signals and Slots
        self.size_x.textChanged.connect(self.changeHorizontalContents)
        self.fontsize_x.valueChanged.connect(self.changeHorizontalContents)
        self.fontsize_y.valueChanged.connect(self.changeVerticalContents)
        self.size_y.textChanged.connect(self.changeVerticalContents)
        self.max_y.textChanged.connect(self.changeVerticalContents)
        self.min_y.textChanged.connect(self.changeVerticalContents)
        self.rotation_x.textChanged.connect(self.changeHorizontalContents)
        self.intervalo.textChanged.connect(self.changeHorizontalContents)
        self.unidade.activated.connect(self.changeHorizontalContents)

    def changeVerticalContents(self):
        size = self.size_y.value()
        min_ = self.min_y.value()
        max_ = self.max_y.value()
        fontsize = self.fontsize_y.value()
        this = {"size" : size, "min_": min_, "max_": max_, "fontsize":fontsize}
        self.parentWidget.canvas.smart_yticks(**this)
        self.updateProperties()
        return None

    def changeHorizontalContents(self):
        size = self.size_x.value()
        rotation = self.rotation_x.value()
        intervalo = self.intervalo.value()
        range_format = self.unidade.currentText()
        fontsize = self.fontsize_x.value()
        this = {"size": size, "rotation": rotation, "fontsize" : fontsize,
                "daterange": intervalo, "dateformat": range_format}
        self.parentWidget.canvas.smart_xticks(**this)
        self.updateProperties()
        return None

    def updateProperties(self):
        self.max_y.setValue(self.parentWidget.canvas.ytick_max)
        self.min_y.setValue(self.parentWidget.canvas.ytick_min)
        self.max_x.setValue(self.parentWidget.canvas.xtick_max)
        self.min_x.setValue(self.parentWidget.canvas.xtick_min)
        return None

    def run(self):
        items = self.items_timeseries
        if self.active_scatter: items = self.items_scatterplot
        TreeWidgetItems = []
        widgets = self.widgets[self.active_scatter]
        for key in widgets.keys():
            item = QTreeWidgetItem([key])
            TreeWidgetItems.append(item)

        self.insertTopLevelItems(0, TreeWidgetItems)
        j = 0
        for key, values in widgets.items():
            for i in range(len(values)):
                properties = items[key][i]
                child = QTreeWidgetItem()
                child.setText(0, properties)
                TreeWidgetItems[j].addChild(child)
                self.setItemWidget(child, 1, values[i])

            j += 1
        
        return None


class PropriedadesTab(QWidget):

    def __init__(self, canvas = None):
        super().__init__()
        self.canvas = canvas

        # Widgets
        self.rotulos = ["Título do gráfico", "Título (eixo horizontal)",
                        "Título (eixo vertical)"]
        self.ax_properties = [".title", ".xaxis.get_label()",
                            ".yaxis.get_label()"]
        self.eixos = TabelaEixos(parentWidget = self)
        formatGroup = QGroupBox("Formatação")
        self.bold = QPushButton(text = "B")
        self.elementos = QComboBox()
        self.textline = QLineEdit()
        self.fontsize = QSpinBox()
        #
        self.legend_colors = QTableWidget()
        legendGroup = QGroupBox("Legenda")
        self.legend_cols = QSpinBox()
        self.legend_fontsize = QSpinBox()
        #
        self.aplicar_limite = QPushButton(text = "Aplicar")
        LimiteGroup = QGroupBox("Faixa de Limite")
        TipoGroup = QGroupBox("Tipo de gráfico")
        self.legend_limite = QLineEdit()
        self.grafico_tipo = QComboBox()
        self.check_limite = QCheckBox()
        self.value_limite = QSpinBox()
        self.nome_limite = QLineEdit()
        
        # configurando widgets
        self.bold.setStyleSheet("font-weight: bold")
        self.elementos.addItems(self.rotulos)
        self.fontsize.setRange(1, 50)
        self.bold.setCheckable(True)
        #
        self.legend_cols.setRange(1, 10)
        self.legend_cols.setValue(5)
        self.legend_fontsize.setRange(1, 30)
        self.legend_fontsize.setValue(10)
        #
        self.grafico_tipo.addItems(["Gráfico de linha", "Gráfico de barra", 
                                    "Gráfico de ultrapassagens"])
        self.value_limite.setMaximum(10000)

        # Layouts
        FormatLayout = QVBoxLayout()
        FormatLayout.addWidget(self.elementos)
        FormatLayout2 = QHBoxLayout()
        FormatLayout2.addWidget(self.textline)
        FormatLayout2.addWidget(self.fontsize)
        FormatLayout2.addWidget(self.bold)
        FormatLayout.addLayout(FormatLayout2)
        FormatLayout.addWidget(QLabel("Elementos dos eixos"))
        FormatLayout.addWidget(self.eixos)
        formatGroup.setLayout(FormatLayout)
        #
        positionLayout = QHBoxLayout()
        positionLayout.addWidget(QLabel("Colunas"))
        positionLayout.addWidget(self.legend_cols)
        positionLayout.addWidget(QLabel("Tamanho"))
        positionLayout.addWidget(self.legend_fontsize)
        positionLayout.setStretch(1, 2)
        displayLayout = QVBoxLayout()
        displayLayout.addLayout(positionLayout)
        displayLayout.addWidget(self.legend_colors)
        legendGroup.setLayout(displayLayout)
        #
        SubLayout = QVBoxLayout()
        TipoLayout = QHBoxLayout()
        TipoLayout.addWidget(self.grafico_tipo)
        TipoGroup.setLayout(TipoLayout)
        LimiteLayout = QGridLayout()
        LimiteLayout.addWidget(QLabel("Incluir?"), 0, 0)
        LimiteLayout.addWidget(self.check_limite, 0, 1)
        LimiteLayout.addWidget(QLabel("Valor"), 1, 0)
        LimiteLayout.addWidget(self.value_limite, 1, 1)
        LimiteLayout.addWidget(QLabel("Legenda"), 2, 0)
        LimiteLayout.addWidget(self.legend_limite, 2, 1)
        LimiteLayout.addWidget(self.aplicar_limite, 3, 0, 3, 2)
        LimiteGroup.setLayout(LimiteLayout)
        SubLayout.addWidget(TipoGroup)
        SubLayout.addWidget(LimiteGroup)
        #
        MainLayout = QHBoxLayout()
        MainLayout.addLayout(SubLayout)
        MainLayout.addWidget(formatGroup)
        MainLayout.addWidget(legendGroup)
        MainLayout.setStretch(1, 2)
        MainLayout.setStretch(2, 2)
        self.setLayout(MainLayout)

        # Signals and Slots
        self.legend_colors.cellDoubleClicked.connect(self.choose_color)
        self.legend_cols.valueChanged.connect(self.updateLegendFormat)
        self.legend_fontsize.valueChanged.connect(self.updateLegendFormat)
        self.elementos.activated.connect(self.format_options)
        self.textline.editingFinished.connect(self.set_label)
        self.fontsize.valueChanged.connect(self.set_fontsize)
        self.bold.clicked.connect(self.set_bold)

        # chamando funcoes
        self.format_options()

    def updateLegendFormat(self):
        ncols = self.legend_cols.value()
        size = self.legend_fontsize.value()
        self.canvas.updateLegend(self.legend_limite.text(), ncols, size)
        return None

    def choose_color(self, row, column):
        if column != 1:
            pass
        item = self.legend_colors.item(row, column)
        Color = item.background().color()
        name = self.legend_colors.item(row, 0).text()
        color_picker = QColorDialog().getColor(Color, title = "Gerenciador de cores")
        if color_picker.isValid():
            rgba = color_picker.getRgb()
            item.setBackground(QColor.fromRgb(*rgba))
            self.canvas.updateColor(name, tuple(i/255 for i in rgba))
            ncols = self.legend_cols.value()
            self.canvas.updateLegend(self.legend_limite.text(), ncols)
        return None

    def set_label(self):
        ax_properties = [".label", ".xlabel", ".ylabel"]
        text = eval("self.canvas.axes{}".format(self.ax_properties[self.elementos.currentIndex()]))
        novo_texto = self.textline.text()
        text.set_text(novo_texto)
        exec("self.canvas{} = novo_texto".format(ax_properties[self.elementos.currentIndex()]))
        self.canvas.draw()
        return None

    def set_fontsize(self):
        ax_properties = [".label", ".xlabel", ".ylabel"]
        text = eval("self.canvas.axes{}".format(self.ax_properties[self.elementos.currentIndex()]))
        text.set_fontsize(self.fontsize.value())
        exec("self.canvas{}_fontsize = {}".format(ax_properties[self.elementos.currentIndex()], self.fontsize.value()))
        self.canvas.draw()
        return None

    def set_bold(self):
        ax_properties = [".label", ".xlabel", ".ylabel"]
        text = eval("self.canvas.axes{}".format(self.ax_properties[self.elementos.currentIndex()]))
        fontweight = ["normal", "bold"]
        boolean = self.bold.isChecked()
        text.set_fontweight(fontweight[boolean])
        exec("self.canvas{}_fontweight = fontweight[boolean]".format(ax_properties[self.elementos.currentIndex()]))
        self.canvas.draw()
        return None

    def format_options(self):
        ax_properties = [".label", ".xlabel", ".ylabel"]
        idx = ax_properties[self.elementos.currentIndex()]
        self.textline.setText(
            eval("self.canvas{}{}".format(idx, "")))
        self.fontsize.setValue(
            eval("self.canvas{}{}".format(idx, "_fontsize")))
        self.bold.setChecked(
            eval("self.canvas{}{}".format(idx, "_fontweight"))== "bold")
        return None

    def stretchHeader(self):
        Header = self.legend_colors.horizontalHeader()
        Header.setSectionResizeMode(QHeaderView.Stretch)
        Header.resizeSections()
        return None

    def update_table(self):
        i = 0
        colors = self.canvas.colors
        handles, labels = self.canvas.axes.get_legend_handles_labels()
        self.legend_colors.setRowCount(len(labels))
        self.legend_colors.setColumnCount(2)
        self.legend_colors.setHorizontalHeaderLabels(["Nome",
            "Cor da Legenda"])
        for label in labels:
            if self.legend_limite.text() == label:
                label = "Faixa Limite"
            item_name = QTableWidgetItem(label)
            item_color = QTableWidgetItem()
            temp = (np.array(colors[label])*255).astype(int)
            item_color.setBackground(QColor.fromRgb(*temp))
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            item_color.setFlags(item_color.flags() & ~Qt.ItemIsEditable)
            self.legend_colors.setItem(i, 0, item_name)
            self.legend_colors.setItem(i, 1, item_color)
            i += 1

        self.stretchHeader()
        return None


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Propriedades da janela
        self.setWindowTitle("ArES")
        self.resize(1000, 700) # largura, altura
        self.logo_icon = QIcon()
        self.logo_icon.addFile(".\\icons\\logo.ico")
        self.setWindowIcon(self.logo_icon)

        # variaveis criadas para o gerenciamento da janela
        self.save_dir = os.path.expanduser(mpl.rcParams['savefig.directory'])
        self.ds = None
        self.results = {}
        self.signature = []
        self.arquivos = []
        self.inventory = data_management.Inventario(parent = self)
        self.lista_calculo = ["Nenhum",  "Média móvel", "Média aritmética",
                                "Média geométrica", "Média harmônica"]
        self.representatividade = {
            "Diária": 75,
            "Mensal": 75,
            "Anual": 50,
            "No período": 0,
            "Média móvel": 75,
            "Geral" : 75
        }

        # Widget Principal
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # Outros Widgets
        self.dataset_dialog = DatasetDialog(self)
        self.botao_abrir = QPushButton("Adicionar")
        self.botao_remover = QPushButton("Remover")
        self.botao_limpar = QPushButton("Limpar")
        self.botao_configs = QPushButton("Configurações")
        self.botao_processar = QPushButton("Processar")
        self.tabela = Tabela(self)
        self.data_ini = QDateEdit(QDate.currentDate().addMonths(-1))
        self.data_fim = QDateEdit(QDate.currentDate())
        self.user_operations = OperationsTable(self)
        save_icon = QIcon.fromTheme("document-save",
                                    QIcon(".\\icons\\icon_save.ico"))
        saveAct = QAction(save_icon, "Salvar como tabela...", self)
        saveAct.triggered.connect(self.exportar_excel)

        # Canvas Matplotlib
        self.canvas = graphictools.MplCanvas(self)
        self.toolbar = graphictools.NavigationToolbar(self.canvas, self)
        self.toolbar.addAction(saveAct)
        
        # Tab Dados
        DadosLayout = QHBoxLayout()
        TabelaLayout = QVBoxLayout()
        ButtonTabelaLayout = QHBoxLayout()
        #
        ButtonTabelaLayout.addWidget(self.botao_abrir)
        ButtonTabelaLayout.addWidget(self.botao_remover)
        ButtonTabelaLayout.addWidget(self.botao_limpar)
        #
        TabelaLayout.addLayout(ButtonTabelaLayout)
        TabelaLayout.addWidget(self.tabela)
        #
        DataLayout = QHBoxLayout()
        DataLayout.addWidget(QLabel("Período: "))
        DataLayout.addWidget(self.data_ini)
        DataLayout.addWidget(QLabel(" a "))
        DataLayout.addWidget(self.data_fim)
        DataLayout.addStretch(5)
        DataLayout.addWidget(self.botao_configs)
        DataLayout.addWidget(self.botao_processar)
        #
        ParametrosLayout = QGridLayout()
        ParametrosLayout.addLayout(DataLayout, 0, 1)
        ParametrosLayout.setColumnStretch(1, 10)
        ParametrosLayout.addWidget(self.user_operations, 2, 1)
        #
        DadosLayout.addLayout(TabelaLayout)
        DadosLayout.addLayout(ParametrosLayout)
        #
        self.DadosTab = QWidget()
        self.DadosTab.setLayout(DadosLayout)

        # Tab Widget
        self.tab = QTabWidget()
        self.GraficoTab = PropriedadesTab(self.canvas)
        self.tab.addTab(self.DadosTab, "Dados")
        self.tab.addTab(self.GraficoTab, "Gráfico")
        
        # Layout principal (central) do programa
        MainLayout = QGridLayout()
        MainLayout.addWidget(self.tab, 2, 0)
        MainLayout.addWidget(self.canvas, 1, 0)
        MainLayout.addWidget(self.toolbar, 0, 0)
        MainLayout.setRowStretch(1, 4)
        MainLayout.setRowStretch(2, 1)
        widget.setLayout(MainLayout) # Coloca o Layout principal na Janela (Importante)

        # Signals and Slots
        self.botao_abrir.clicked.connect(self.openDatasetWindow)
        self.botao_remover.clicked.connect(self.remover_arquivo)
        self.botao_limpar.clicked.connect(self.clean_files)
        self.botao_processar.clicked.connect(self.processar)
        self.GraficoTab.aplicar_limite.clicked.connect(self.updateGraph)
        self.GraficoTab.grafico_tipo.currentTextChanged.connect(self.updateGraph)
        self.botao_configs.clicked.connect(self.openConfigWindow)

    def openConfigWindow(self):

        dialog = MyDialog(self)
        dialog.show()
        dialog.exec()

    def openDatasetWindow(self):
        if not self.dataset_dialog.isVisible():
            self.dataset_dialog.show()
            self.dataset_dialog.exec()

        else:
            self.dataset_dialog.setWindowState(Qt.WindowNoState)
        return None

    def processar(self):
        ini = self.data_ini.date().toPython()
        fim = self.data_fim.date().toPython()

        # checa por inconsistencias
        n = len(self.arquivos)
        
        # Testes de verificacao
        # se nenhum arquivo foi aberto, notifique o usuario
        if n == 0:
            x = QMessageBox(QMessageBox.Warning, "Erro",
                     'Não é possível realizar o processamento', parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText("Por favor, adicione pelo menos um conjunto de dados.")
            x.exec()
            return None

        # se a data inicial for maior que a final
        elif ini > fim:
            x = QMessageBox(QMessageBox.Warning, "Erro",
                    'Não é possível realizer o processamento', parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText("A data final especificada é menor do que a data inicial.")
            x.exec()
            return None
        
        # ao passar os testes
        station_types = [0]*n
        for i in range(n):
            station_types[i] = self.arquivos[i].tipo
        unique_type = np.unique(station_types)

        # se estacoes de tipos diferentes forem adicionadas
        if unique_type.shape[0] > 1:
            x = QMessageBox(QMessageBox.Warning, "Erro",
            'Não é possível realizar o processamento com tipos de estações diferentes.',
            parent = self
            )
            x.addButton(QMessageBox.Ok)
            x.setInformativeText(
                "Por favor, mantenha aberto no programa somente estações de monitoramento do mesmo tipo."
                )
            x.exec()
            return None

        # Operacoes
        try:
            # provoca um erro se nenhum paramtro for selecionado
            self.ds = utilitarios.organize(self, ini, fim, unique_type[0])
        except:
            x = QMessageBox(QMessageBox.Warning, "Erro",
                    'Não é possível realizar o processamento', parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText("Por favor, selecione pelo menos um parâmetro.")
            x.exec()
            return None

        utilitarios.rotina_operacoes(self, unique_type[0])
        gc.collect() # Chama o coletor de lixo, para liberar espaço

        # prepara os resultados, segundo a representatividade, e checa se os
        # as series de dados resultantes nao estao vazias
        lim = self.get_lim()
        self.results = self.ds.mask_invalidos(lim)
        if self.ds.is_empty(self.results):
            x = QMessageBox(QMessageBox.Critical, "Erro", "Dados inválidos", parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText('A série de dados se encontra vazia '
                                'ou composta somente por dados inválidos.')
            x.exec()
            return None

        # finalmente plota, se nao houver problemas
        self.updateGraph()

    def clean_files(self):
        self.arquivos = []
        self.signature = []
        self.ds.clear()
        
        # Libera memoria de objetos nao referenciados
        gc.collect()
        self.tabela.update()
    
    def get_lim(self):
        groupby = self.ds.agrupar
        if len(groupby) == 0:
            ultima_operacao = "Geral"
        
        else:
            time_freq = ["Diária", "Mensal", "Anual"]
            known_freq = ["Dia", "Mês", "Ano"]
            freq_dict = dict(zip(known_freq, time_freq))
            
            ultima_operacao = groupby[-1].split(" ")[0]
            ultima_operacao = freq_dict.get(ultima_operacao, "Geral")

        lim = self.representatividade[ultima_operacao]
        return lim

    def updateGraph(self):
        if self.ds != None:
            graphTypes = [
                self.canvas.linePlot,
                self.canvas.barPlot,
                self.canvas.ultrapassagensPlot
                ]
            graphTypes[self.GraficoTab.grafico_tipo.currentIndex()](
                self.ds, self.results
                )

        if self.GraficoTab.check_limite.isChecked():
            value = self.GraficoTab.value_limite.value()
            self.canvas.hline_faixa(value, "Faixa limite")

        label = self.GraficoTab.legend_limite.text()
        ncols = self.GraficoTab.legend_cols.value()
        size = self.GraficoTab.legend_fontsize.value()
        self.canvas.updateLegend(label, ncols, size)
        self.GraficoTab.eixos.updateProperties()
        self.GraficoTab.update_table()

        return True
    
    def remover_arquivo(self):
        ''' comando para remover as estacoes ja abertas no programa
        conforme selecionadas na tabela.'''
        # Esse metodo varre toda a tabela em busca do selecionado.
        for i in range(len(self.arquivos)):
            TopLevelItem = self.tabela.items[i]
            if TopLevelItem.isSelected():
                entity_idx = TopLevelItem.child(0).data(1, 0)
                del self.signature[entity_idx] # quem é ? nao lembro para que serve
                del self.arquivos[entity_idx]

        # Libera memoria de objetos nao referenciados
        gc.collect()

        # atualiza a tabela
        self.tabela.update()

    def exportar_excel(self):
        startpath = self.save_dir
        start = os.path.join(startpath)
        fname, filter = QFileDialog.getSaveFileName(
            parent = self,
            caption = "Salvar tabela como...",
            dir = start,
            filter = "Excel files (*.xlsx)",
        )
        if len(fname) > 0 and self.ds.shape[0] > 0:
            self.save_dir = os.path.dirname(fname)
            utilitarios.save_excel(self.ds, fname)

    def closeEvent(self, event) -> None:
        if not self.dataset_dialog.isHidden():
            self.dataset_dialog.close()

        self.inventory.disconnect()
        return super().closeEvent(event)


class MyDialog(QDialog):

    def __init__(self, master):
        QDialog.__init__(self)
        self.master = master
        self.setWindowTitle("Configurações")
        self.setFixedSize(500, 300)
        self.setModal(True)
        self.setWindowIcon(master.logo_icon)

        # Widgets
        self.WidgetRepresentatividade = QTableWidget()
        self.valueRepresentatividade = {}
        self.salvar = QPushButton("Aplicar")
        self.fechar = QPushButton("Cancelar")
        group = QGroupBox("Conexão do banco de dados", parent = self)
        self.username_widget = QLineEdit(group)
        self.password_widget = QLineEdit(group)
        self.connect_button = QPushButton("Conectar")
        
        self.hostname = QLineEdit(self.master.inventory.host)

        # Configuracoes dos Widgets
        self.hostname.setReadOnly(True)
        self.password_widget.setEchoMode(QLineEdit.EchoMode.Password)
        Header = self.WidgetRepresentatividade.horizontalHeader()
        Header.setSectionResizeMode(QHeaderView.Stretch)
        Header.resizeSections()
        self.WidgetRepresentatividade.setColumnCount(2)
        self.WidgetRepresentatividade.setHorizontalHeaderLabels(["Representatividade", "Valor (%)"])
        for k, v in master.representatividade.items():
            self.valueRepresentatividade[k] = QSpinBox()
            self.valueRepresentatividade[k].setRange(0, 100)
            self.valueRepresentatividade[k].setValue(v)
        self.WidgetRepresentatividade.setRowCount(len(self.valueRepresentatividade))
        self.runWidget()
        
        # Layouts
        Layout = QHBoxLayout()
        Layout.addWidget(self.salvar)
        Layout.addWidget(self.fechar)
        #
        LoginLayout = QGridLayout()
        LoginLayout.addWidget(QLabel(text = "Host"), 0, 0)
        LoginLayout.addWidget(QLabel(text = "Usuário"), 1, 0)
        LoginLayout.addWidget(QLabel(text = "Senha"), 2, 0)
        LoginLayout.addWidget(self.hostname, 0, 1, 1, 2)
        LoginLayout.addWidget(self.username_widget, 1, 1, 1, 2)
        LoginLayout.addWidget(self.password_widget, 2, 1, 1, 2)
        LoginLayout.addWidget(self.connect_button, 3, 2)
        group.setLayout(LoginLayout)
        LoginLayout.setRowStretch(4, 5)
        #
        MainLayout = QGridLayout()
        MainLayout.addWidget(self.WidgetRepresentatividade, 0, 0)
        MainLayout.addWidget(group, 0, 1)
        MainLayout.addLayout(Layout, 1, 1)
        #
        self.setLayout(MainLayout)

        # Signals and Slots
        self.salvar.clicked.connect(self.saveAndClose)
        self.fechar.clicked.connect(self.close)
        self.connect_button.clicked.connect(self.connect_sql)

    def connect_sql(self):
        username = self.username_widget.text()
        password = self.password_widget.text()
        code = self.master.inventory.connect(username, password)
        if code != 1:
            if code == 1045:
                message = "Acesso negado."
                informative_text = "Login ou senha estão errados."
            elif code == 2005:
                message = "Erro de conexão."
                informative_text = "O host não existe ou se encontra offline."
            x = QMessageBox(QMessageBox.Warning, "Erro",
                    message, parent = self.master)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText(informative_text)
            x.exec()
        else:
            message = "Conetado."
            informative_text = "A conexão com o servidor foi estabelecida."
            x = QMessageBox(parent = self.master)
            x.setText(message)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText(informative_text)
            x.exec()
        
        self.master.dataset_dialog.search_empresas()

        return None

    def runWidget(self):
        i = 0
        for k, v in self.valueRepresentatividade.items():
            self.WidgetRepresentatividade.setCellWidget(i, 1, v)
            item = QTableWidgetItem(k)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.WidgetRepresentatividade.setItem(i, 0, item)
            i += 1

    def saveAndClose(self):
        ''' Salva as modificacoes e fecha a janela'''
        for k, v in self.valueRepresentatividade.items():
            self.master.representatividade[k] = v.value()

        self.close()


class DatasetDialog(QDialog):

    def __init__(self, master):
        QDialog.__init__(self)
        self.master = master
        self.setWindowTitle("Importar dados")
        self.setFixedSize(400, 200)
        # self.setWindowIcon(QIcon(r'images\icon6.ico'))
        self.setModal(False)
        self.setWindowIcon(master.logo_icon)

        # Widgets
        add_button = QPushButton("Adicionar")
        cancel_button = QPushButton("Cancelar")
        browse_button = QPushButton("...")
        BuscaTab = QWidget()
        ImportTab = QWidget() 
        self.empresas = QComboBox(BuscaTab)
        self.entidades = QComboBox(BuscaTab)
        self.atmos_path = QLineEdit("")

        # Tab Widget
        self.tab = QTabWidget()
        self.tab.addTab(BuscaTab, "Buscar")
        self.tab.addTab(ImportTab, "Importar [ATMOS]")

        # Configuracoes dos Widgets
        self.search_empresas()
        self.atmos_path.setReadOnly(True)

        # Layouts
        busca_layout = QVBoxLayout()
        busca_layout.addWidget(QLabel("Empresa"))
        busca_layout.addWidget(self.empresas)
        busca_layout.addWidget(QLabel("Entidade"))
        busca_layout.addWidget(self.entidades)
        BuscaTab.setLayout(busca_layout)
        busca_layout.insertSpacing(-1, 100)
        #
        import_atmos_layout = QVBoxLayout()
        import_atmos_layout.addWidget(QLabel("Selecionar arquivo"))
        secondary_layout = QHBoxLayout()
        secondary_layout.addWidget(self.atmos_path)
        secondary_layout.addWidget(browse_button)
        import_atmos_layout.addLayout(secondary_layout)
        import_atmos_layout.insertSpacing(-1, 100)
        ImportTab.setLayout(import_atmos_layout)
        #
        layout = QVBoxLayout()
        layout.addWidget(self.tab)
        saveclose_layout = QHBoxLayout()
        saveclose_layout.addWidget(add_button)
        saveclose_layout.addWidget(cancel_button)
        saveclose_layout.insertSpacing(0, 150)
        layout.addLayout(saveclose_layout)
        self.setLayout(layout)

        # Signals and Slots
        add_button.clicked.connect(self.add)
        cancel_button.clicked.connect(self.close)
        self.empresas.currentTextChanged.connect(self.search_entidades)
        browse_button.clicked.connect(self.browse_xls_files)

    def browse_xls_files(self):
        '''o comando abaixo abre uma janela para selecao do arquivo e
            retorna o caminho ate ele. Se o usuario fechar a janela
            retorna uma string vazia'''
        startpath = self.master.save_dir
        start = os.path.join(startpath)
        caminho, x = QFileDialog.getOpenFileNames(self, "Selecione um arquivo",
            filter = "Excel files (*.xls)",
            dir = start
        )
        self.atmos_path.setText(str(caminho)[1:-1])

    def add(self):
        if self.tab.currentIndex() == 0:
            if not self.master.inventory.get_status():
                return None
            nome = self.entidades.currentText()
            if not nome in self.master.signature:
                self.master.arquivos.append(
                    self.master.inventory.extrair_estacao(nome))
                self.master.signature.append(nome)
        else:
            caminho = eval('['+self.atmos_path.text()+']')
            if len(caminho) > 0:
                self.master.save_dir = os.path.dirname(caminho[0])
                for filepath in caminho:
                    if filepath in self.master.signature: continue
                    try:
                        self.master.arquivos.append(utilitarios.xls2file(filepath))
                        self.master.signature.append(filepath)
                    except:
                        continue

        self.master.tabela.update()
        return None

    def search_empresas(self):
        empresas = self.master.inventory.estacao_empresas
        self.empresas.clear()
        self.empresas.addItems(np.unique(empresas))
        self.search_entidades(self.empresas.currentText())
        return None

    @Slot(str)
    def search_entidades(self, empresa):
        empresas = np.array(self.master.inventory.estacao_empresas)
        if empresas.shape[0] > 0:
            entidades = np.array(self.master.inventory.estacao_nomes)[empresas == empresa]
            self.entidades.clear()
            self.entidades.addItems(entidades)

        return None


class OperationsTable(QTableWidget):

    def __init__(self, master):
        super().__init__(master)
        
        # propriedades da tabela
        self.setRowCount(1)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(
            ["", "Operação", "Agrupar por"]
            )
        Header = self.horizontalHeader()
        Header.setSectionResizeMode(1, QHeaderView.Stretch)
        Header.setSectionResizeMode(2, QHeaderView.Stretch)
        Header.resizeSections()
        
        # variaveis da classe
        self.row_track = 0 # controle da linha onde "+" esta
        self.lista_calculo = ["Média móvel", "Média aritmética",
                            "Média geométrica", "Média harmônica",
                            "Máximo"]
        self.agrupar = ["Não agrupar", "Dia", "Mês e ano", "Ano"]

        # widgets
        self.add_button = QPushButton(text = "+")
        self.blank_cell1 = QTableWidgetItem()
        self.blank_cell2 = QTableWidgetItem()

        # configura widget
        self.setCellWidget(self.row_track, 0, self.add_button)
        self.blank_cell1.setFlags(self.blank_cell1.flags() & ~Qt.ItemIsEditable)
        self.blank_cell2.setFlags(self.blank_cell2.flags() & ~Qt.ItemIsEditable)
        self.setItem(self.row_track, 1, self.blank_cell1)
        self.setItem(self.row_track, 2, self.blank_cell2)

        # Signals and slots
        self.add_button.clicked.connect(self.create_filled_row)
        self.resizeColumnToContents(0)

    def create_filled_row(self):
        # Inserir linha
        self.insertRow(self.row_track)

        # cria widgets
        remove_button = QPushButton(text = "-")
        operation_combo = QComboBox()
        groupby_combo = QComboBox()

        # configura widgets
        operation_combo.addItems(self.lista_calculo)
        groupby_combo.addItems(["8 horas"])
        self.setCellWidget(self.row_track, 0, remove_button)
        self.setCellWidget(self.row_track, 1, operation_combo)
        self.setCellWidget(self.row_track, 2, groupby_combo)

        # signals and slots
        remove_button.clicked.connect(
            self.delete_row
            )
        operation_combo.currentTextChanged.connect(
            self.update_operation_box
        )
        self.row_track += 1

        return None

    def update_operation_box(self):
        row = self.currentRow()
        combobox = self.cellWidget(row, 1)

        is_media_movel = combobox.currentIndex() == 0
        group_combobox = self.cellWidget(row, 2)
        if is_media_movel:
            group_combobox.clear()
            group_combobox.addItems(["8 horas"])
        
        elif group_combobox.count() == 1:
            group_combobox.clear()
            group_combobox.addItems(self.agrupar)
        
        return None

    def delete_row(self):
        self.removeRow(self.currentRow())
        self.row_track -= 1

        return None

def main():
    # marca o diretorio do script como atual
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    
    # inicia a aplicacao
    myappid = 'inea.ArES.1a' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()

    # estilos do programa
    # print(QFontDatabase().families())
    # with open("./styles/styles.qss", "r") as f:
    #     _style = f.read()
    #     app.setStyleSheet(_style)

    # executa o programa
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    