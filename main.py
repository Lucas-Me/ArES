# IMPORT MODULES
import sys, os
import locale

# IMPORT QT CORE
from qt_core import *

# IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import UI_MainWindow

# IMPORT DIALOG
from gui.windows.dialog.import_dialog import ImportDialog
from gui.windows.dialog.splash_screen import SplashScreen

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'inea.ares.1.3.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class LoadUi(QObject):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.mainWindow = parent

    @Slot()
    def start(self):
        # load the main UI
        self.mainWindow.ui = UI_MainWindow()
        self.mainWindow.ui.setup_ui(self.mainWindow)
        left_menu = self.mainWindow.ui.left_menu

        # open page 1
        left_menu.btn_home.clicked.connect(lambda: self.mainWindow.change_page(page = 0, button = left_menu.btn_home))
        
        # open page 2
        left_menu.btn_data.clicked.connect(lambda: self.mainWindow.change_page(page = 1, button = left_menu.btn_data))

        # open page 3
        left_menu.btn_process.clicked.connect(lambda: self.mainWindow.change_page(page = 2, button = left_menu.btn_process))

        # SQL request
        self.mainWindow.ui.pages.data_page.ui.sql_btn.clicked.connect(self.mainWindow.updateDatabaseSQL)

        # NEXT button on DATA MANAGER SCREEEn
        self.mainWindow.ui.pages.data_page.ui.next_btn.clicked.connect(self.mainWindow.requestData)

        # PROCESS button on PROCESS SCREEn
        self.mainWindow.ui.pages.process_page.resultReady.connect(self.mainWindow.updateDataHandles)

        # EMIT SIGNAL
        self.mainWindow.uiLoaded.emit()

# MAIN WINDOW
class MainWindow(QMainWindow):
    uiLoaded = Signal()

    def __init__(self) -> None:
        super().__init__()

        # PROPERTIES
        self.version = '1.3.1'

        # window title
        self.setWindowTitle("ArES")

        # UI LOADING ON DEDICATE THREAD
        # //////////////////////////////
        self.uiLoadingThread = QThread()

        # create and show the splash screen
        self.loadingScreen = SplashScreen()
        self.loadingScreen.show()

        # creating the QObject
        self.loadUI = LoadUi(self)

        # SIGNALS AND SLOTS
        # connect the ui loaded signal
        self.uiLoaded.connect(self.closeLoadingScreen)
        self.uiLoaded.connect(self.uiLoadingThread.quit)
        self.uiLoaded.connect(self.loadUI.deleteLater)

        # connet the start
        self.uiLoadingThread.started.connect(self.loadUI.start)
        
        # Start the UI Loading
        self.uiLoadingThread.start()

    def closeLoadingScreen(self):
        # show the main UI
        self.show()

        # Close the loading screen
        self.loadingScreen.close()

    def reset_menu_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            if btn.objectName() in ['home', 'settings', 'data', 'methods', 'chart']:
                btn.setActive(False)

    def change_page(self, page, button : QPushButton):
        if isinstance(page, int):
            if page == 2:
                # check if there is at least one parameter loaded
                n = len(self.ui.pages.process_page.raw_data)
                if n == 0:
                    return None

            # Change page
            self.ui.pages.setCurrentIndex(page)

        else: # not an int
            self.ui.pages.setCurrentWidget(page)

        # Change page
        self.reset_menu_selection()
        button.setActive(True)

    def updateDatabaseSQL(self):
        server = self.ui.pages.login_page.sql
        if not server.get_status(): # if not connected, display window
            self.connnectionErrorDialog()
            return None

        # browser sql files
        self.ui.pages.data_page.browse_sql(server)

    def requestData(self):
        # getting server
        server = self.ui.pages.login_page.sql

        # requesting data
        data_manager = self.ui.pages.data_page

        try:
            data, start_date, end_date = data_manager.request_data(server)

        except TimeoutError as err: # se der erro, provavelmente a conexao foi perdida
            self.connnectionErrorDialog()
            return None

        # updating data on processing screen
        self.ui.pages.process_page.updateRawData(data)
        self.ui.pages.process_page.updateDates(start_date, end_date)

        # force click on third screen (left menu)
        self.ui.left_menu.btn_process.click()

    @Slot(list)
    def updateDataHandles(self, processed_data : list[object]):
        target = self.ui.pages
        target.updateDataHandles(processed_data)

    def connnectionErrorDialog(self):
        '''
        Janela de Dialogo quando ocorre algum problema na conexão SQL.
        '''
        self.ui.pages.login_page.disconnectSQL()
        dialog = ImportDialog(
            title = 'Erro',
            message = 'Não foi possível se comunicar com o banco de dados',
            description='Certifique-se de que a conexão esteja estabelecida',
            parent = self
        )
        dialog.okClicked.connect(lambda: self.change_page(page = 0, button = self.ui.left_menu.btn_home))
        dialog.exec()


if __name__ == "__main__":
    # marca o diretorio do script como atual
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)

    # locale (linguagem do sistema)
    locale.setlocale(locale.LC_ALL, 'pt_BR')

    # criando aplicacao
    app = QApplication(sys.argv)

    # window icon
    icon_pixmap = QPixmap(get_imagepath('ArES_logo.ico', 'gui/images/icons'))
    icon = QIcon(icon_pixmap)
    app.setWindowIcon(icon)
    
    # run application main window
    window = MainWindow()
    sys.exit(app.exec())