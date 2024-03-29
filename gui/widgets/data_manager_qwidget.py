# IMPORTS
import os, re, datetime
import numpy as np

# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_data_page import UI_DataManager
from gui.windows.dialog.file_dialog import FileDialog
from gui.windows.dialog.loading_dialog import LoadingDialog
from gui.windows.dialog.import_dialog import ImportDialog

# IMPORT CUSTOM MODULES
from backend.data_management.functions import xls_reader, get_dateindex, reindex
from backend.data_management.data_management import SQlStationData, RawData

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import find_unit

# Data Manager Page Class
class DataManager(QWidget):

    def __init__(self):
        super().__init__()

        # SETUP MAIN UI 
        self.ui = UI_DataManager()
        self.ui.setup_ui(self)
        self.ui.setup_stylesheets(self)
        
        # PROPERTIES
        self.archives = {} # Opened station archives
        self.selected_parameters = {} # selected parameters for each station
        self.browse_folder = os.path.expanduser("~") # user home directory
        self.total_selected = 0 # total number of parameters selected
        self.updateSelectionCount(0)

        # QDialog related properties
        self.file_dialog_code = 0
        self.replicate_command = False

        # SIGNALS AND SLOTS
        self.ui.xls_btn.clicked.connect(self.browse_xls_files)
        self.ui.search_bar.editingFinished.connect(self.search_station)
        self.ui.station_manager_list.itemPressed.connect(self.update_parameter_viewer)
        self.ui.parameter_viewer.stateChanged.connect(self.save_parameter_selection)
        self.ui.clear_btn.clicked.connect(self.clear_station_manager)
        self.ui.clear_sel_btn.clicked.connect(self.clear_selections)
        self.ui.check_box.checked.connect(self.check_parameters)
        self.ui.check_box.unchecked.connect(self.uncheck_parameters)

    def check_parameters(self):
        parameter_viewer = self.ui.parameter_viewer

        # loop thourgh each list item:
        for i in range(parameter_viewer.count()):
            item_widget = parameter_viewer.itemWidget(parameter_viewer.item(i))
            if item_widget.ui.check_box.isChecked():
                continue

            item_widget.ui.check_box.setChecked(True)

    def uncheck_parameters(self):
        parameter_viewer = self.ui.parameter_viewer

        # loop thourgh each list item:
        for i in range(parameter_viewer.count()):
            item_widget = parameter_viewer.itemWidget(parameter_viewer.item(i))
            if not item_widget.ui.check_box.isChecked():
                continue
            
            item_widget.ui.check_box.setChecked(False)

    def clear_selections(self):
        for k, v in self.selected_parameters.items():
            if sum(v) > 0:
                self.selected_parameters[k] = [0] * len(v)

        self.ui.station_manager_list.clear_selections()
        self.uncheck_parameters()

        # update internal count
        self.updateSelectionCount(0)

    def clear_station_manager(self):
        self.ui.station_manager_list.clean_objects()
        #
        self.archives.clear()
        self.selected_parameters.clear()

        # update internal count
        self.updateSelectionCount(0)

    def search_station(self):
        '''
        to do: melhorar esse algoritmo de busca
        '''
        # getting text and setting properties
        text = self.ui.search_bar.text()
        text = text.rstrip().strip()
        chars = len(text)

        # tests
        station_list = self.ui.station_manager_list
        rows = station_list.count()

        if chars > 0:
            prop = text[0] == '@'
            keywords = re.split('\s+', text[prop:].lower())

            for row in range(rows):
                item = station_list.item(row)
                item_widget = station_list.itemWidget(item)
                item.setHidden(True) # assume que todos estejam escondidos
                if item_widget.objectName() == 'item_header' and prop:
                    # search by enterprise
                    sample = re.split('\s+', item_widget.label.lower())
                    
                    tests = []
                    for kw in keywords:
                        tests.append(any(map(lambda element: kw in element, sample)))

                    condition = any(tests)
                    item.setHidden(not condition)

                elif prop:
                    item.setHidden(not condition)

                elif item_widget.objectName() == 'item_header':
                    continue

                else: # search by name
                    sample = re.split('\s+', item_widget._name.lower())
                    tests = []
                    for kw in keywords:
                        tests.append(any(map(lambda element: kw in element, sample)))

                    condition = any(tests)

                    if condition:
                        self.ui.station_manager_list.enterprise_category[item_widget._enterprise].setHidden(False)
                    item.setHidden(not condition)

        else:
            # reset filter
            for row in range(rows):
                station_list.item(row).setHidden(False)

    def updateSelectionCount(self, count):
        self.total_selected = count
        if not count:
            self.ui.next_btn.hide()
        else:
            self.ui.next_btn.show()

    def update_tristate_button(self, active, total):
        if active == 0:
            self.ui.check_box.setCheckState(Qt.CheckState.Unchecked)
        elif active == total:
            self.ui.check_box.setCheckState(Qt.CheckState.Checked)
        else:
            self.ui.check_box.setCheckState(Qt.CheckState.PartiallyChecked)

    def save_parameter_selection(self, args):
        state, row = args
        signature = self.ui.parameter_viewer.get_signature()
        if signature in self.selected_parameters:
            self.selected_parameters[signature][row] = state

        ms = self.ui.station_manager_list
        active_widget = ms.activeWidget
        active_parameters = sum(self.selected_parameters[signature])
        ms.itemWidget(active_widget).marked.updateCount(active_parameters)
        
        # update tristate box
        self.update_tristate_button(active_parameters, len(self.selected_parameters[signature]))

        # # update internal count
        self.updateSelectionCount(self.total_selected + (-1) ** (not state))

    def update_parameter_viewer(self):
        # Save selection of parameters before deleting
        self.ui.parameter_viewer.reset_settings()

        # geting new selected row
        monitoring_list  = self.ui.station_manager_list
        active_widget = self.ui.station_manager_list.activeWidget

        # tests
        if not active_widget is None:
            # get station object
            sig = monitoring_list.itemWidget(active_widget)._signature
            station = self.archives[sig]
            if station.metadata['source'] == 'xls':
                var_list = station.parameters.keys()
            else:
                var_list = station.parameters
            
            # get parameters options
            options = self.selected_parameters[station.metadata['signature']]

            # adding to paramter view widget
            i = 0
            for k in var_list:
                unit = find_unit(k)
                name = k[:k.find(unit) - 1]
                self.ui.parameter_viewer.add_item(
                    name = name,
                    theme = station.parameter_theme[k],
                    unit = unit,
                    selected = options[i]
                )
                i += 1

            # texts on top of list
            fmt =  '%d %b %Y'
            start = station.availability[0].item().strftime(fmt)
            end = station.availability[1].item().strftime(fmt)
            self.ui.information_station.setText(station.metadata['name'])
            self.ui.information_dates.setText(f'{start} - {end}')

            # finishing
            self.ui.parameter_viewer.set_signature(station.metadata['signature'])
            self.ui.check_box.setCheckable(True)

            # toggle tristate button on header
            self.update_tristate_button(sum(options), len(options))

    def browse_xls_files(self):
        file_paths, x = QFileDialog.getOpenFileNames(
            self,
            "Selecione um arquivo",
            filter = "Excel files (*.xls)",
            dir= self.browse_folder
        )

        # file_path is a list with a path to each file.
        if len(file_paths) > 0:
            self.browse_folder = os.path.dirname(file_paths[0])

            # create loading dialog
            dialog = LoadingDialog(text = 'Lendo arquivos', parent = self)
            dialog.show()

            # Create a QThread object
            self.thread = QThread()

            # Create a worker object
            self.worker = Worker(files = file_paths)

            # Move worker to the thread
            self.worker.moveToThread(self.thread)

            # Connect signals and slots
            self.thread.started.connect(self.worker.start_xls)
            #
            self.worker.resultReady.connect(self.thread.quit)
            self.worker.resultReady.connect(self.worker.deleteLater)
            self.worker.resultReady.connect(self.add_files)
            self.worker.resultReady.connect(lambda: dialog.closeWindow(True))
            #
            self.worker.error.connect(self.thread.quit)
            self.worker.error.connect(self.worker.deleteLater)
            self.worker.error.connect(lambda: dialog.closeWindow(False))
            self.worker.error.connect(self.importErrorXLS)
            #
            self.thread.finished.connect(self.thread.deleteLater)

            # Start the thread
            self.thread.start()
                   
    def browse_sql(self, server):
        sql_files = {}
        for i, name in enumerate(server.station_names):
            _object = SQlStationData(
                name = name,
                enterprise = server.station_enterprises[i],
                dates = server.dates[name],
                parameters = server.table_vars[name],
                parameters_cols = server.table_vars_columns[name]
            )
            
            k = _object.metadata['signature']
            sql_files[k] = _object

        self.add_files(sql_files)

    @Slot(dict)
    def add_files(self, files):
        target = self.ui.station_manager_list
        for k, v in files.items():
            if k in self.archives: # se o objeto ja estiver aberto
                if not self.replicate_command:  # pergunta ao usuario o que ele deseja fazer com a duplicata 
                    file_dialog = FileDialog(_object = v, parent= self)
                    file_dialog.exec()
                    
                if self.file_dialog_code == 1: # O usuario escolheu IGNORAR
                    continue
                
                elif self.file_dialog_code == 2: # O usuario escolheu Substituir
                    item = target.getListWidgetItem(k)
                    target.remove_item(item)
                    pass

                else: # O usuario escolheu cancelar a operacao
                    break
            
            # add station into archives
            self.archives[k] = v

            # add parameters list
            self.selected_parameters[k] = [0] * len(v.parameters)

            # add station into list frame
            target.add_station_item(v)

        # reseta a variavel
        self.replicate_command = False

    def importErrorXLS(self):
        '''
        Cria uma janela de dialogo quando ocorre um erro ao efetuar a leitura
        de um ou mais arquivos XLS.
        '''
        dialog = ImportDialog(
            title = 'Erro de leitura',
            message = 'Não foi possível ler um ou mais arquivos',
            description= 'Possivelmente a planilha selecionada não possui a formatação adequada para ser lida no programa.',
            parent = self
        )
        dialog.ok_button.hide()
        dialog.show()

    def request_data(self, server):
        # setting up
        raw_data = [None] * self.total_selected
        start_date, end_date = self.ui.date_edit.getDates()
        end_date = end_date + datetime.timedelta(days = 1) # modificando para ser intervalo fechado

        # loop through archives
        idx = 0
        for sig, v in self.selected_parameters.items():
            # check if there is a paramter selected
            if not any(v):
                continue
            
            # getting object
            _object = self.archives[sig]

            # getting new date array
            new_dates = get_dateindex(
                tipo = _object.metadata['type'],
                freq = _object.metadata['frequency'],
                start_date=start_date,
                end_date=end_date,
                minutos = _object.dates[0].item().minute
            )

            # check if it is either from the XLS or from the SQL
            if sig[:3] == 'xls':
                # loop through selected parameters
                for i, k in enumerate(_object.parameters.keys()):
                    if not self.selected_parameters[sig][i]:
                        continue
                    
                    # recovering arguments
                    metadata = _object.metadata.copy()
                    metadata['parameter'] = k

                    # reindexing the values from arrays
                    values, flags = reindex(_object.dates, _object.parameters[k][0], _object.parameters[k][1], new_dates)
                   
                    # creating object
                    this = RawData(
                        values = values,
                        metadata = metadata,
                        flags = flags,
                        dates = new_dates
                    )

                    # adding to list
                    raw_data[idx] = this
                    idx += 1

            else:
                # loop through selected parameters
                for i, checked in enumerate(self.selected_parameters[sig]):
                    if not checked:
                        continue
                    
                     # recovering arguments
                    metadata = _object.metadata.copy()
                    metadata['parameter'] = _object.parameters[i]

                    # query variables from the SQL Database
                    try:
                        dates, values, flags = server.query_var(
                            var_index = i,
                            station_object = _object,
                            start_date = start_date,
                            end_date = end_date 
                        )
                    except ValueError:
                        # operacao acima retornou objetos vazios.
                        dates = new_dates
                        values = np.full(dates.shape, np.nan)
                        flags = np.full(dates.shape, np.nan)

                    # reindexing the values from arrays
                    values, flags = reindex(dates, values, flags, new_dates)

                    # creating object
                    this = RawData(
                        values = values,
                        metadata = metadata,
                        flags = flags,
                        dates = new_dates
                    )
                    
                    # adding to list
                    raw_data[idx] = this
                    idx += 1

        return raw_data, start_date, end_date - datetime.timedelta(days = 1)

    def paintEvent(self, event: QPaintEvent) -> None:
        # super().paintEvent(event)

        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)


class Worker(QObject):
    '''
    Worker para as tarefas relacionadas a leitura de arquivos XLS e aos processos
    do botao "Proximo"
    '''

    resultReady = Signal(dict)
    error = Signal()

    def __init__(self, **kwargs) -> None:
        super().__init__(kwargs.get('parent', None))
        self.file_paths = kwargs.get('files', None).copy()

    def start_xls(self):
        try:
            xls_files = {}
            for path in self.file_paths:
                # read files and extract information
                files = xls_reader(path)
                xls_files.update(files)
            
            self.resultReady.emit(xls_files)

        except Exception as err:
            # Provavelmente houve erro de leitura em um dos arquivos XLS
            self.error.emit()

        
