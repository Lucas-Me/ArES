# IMPORT MODULES
import sys
import locale

# IMPORT QT CORE
from qt_core import *

# IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import *

# IMPORT DIALGO
from gui.windows.dialog.import_dialog import ImportDialog
from gui.windows.dialog.splash_screen import SplashScreen


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

        # open page 4
        # left_menu.btn_4.clicked.connect(lambda: self.mainWindow.change_page(page = 3, button = self.mainWindow.ui.btn_4))

        # SQL request
        self.mainWindow.ui.ui_pages.data_page.ui.sql_btn.clicked.connect(self.mainWindow.updateDatabaseSQL)

        # NEXT button on DATA MANAGER SCREEEn
        self.mainWindow.ui.ui_pages.data_page.ui.next_btn.clicked.connect(self.mainWindow.requestData)

        # PROCESS button on PROCESS SCREEn
        self.mainWindow.ui.ui_pages.process_page.resultReady.connect(self.mainWindow.updateDataHandles)

        # EMIT SIGNAL
        self.mainWindow.uiLoaded.emit()

# MAIN WINDOW
class MainWindow(QMainWindow):
    uiLoaded = Signal()

    def __init__(self) -> None:
        super().__init__()

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
            if btn.objectName() in ['logo', 'home', 'settings', 'data', 'methods', 'chart']:
                btn.setActive(False)

    def change_page(self, page : int, button : QPushButton):
        if page == 2:
            # check if there is at least one parameter loaded
            n = len(self.ui.ui_pages.process_page.raw_data)
            if n == 0:
                return None
        
        # Change page
        self.reset_menu_selection()
        self.ui.pages.setCurrentIndex(page)
        button.setActive(True)

    def updateDatabaseSQL(self):
        server = self.ui.ui_pages.login_page.sql
        if not server.get_status(): # if not connected, display window
            self.connnectionErrorDialog()
            return None

        # browser sql files
        self.ui.ui_pages.data_page.browse_sql(server)

    def requestData(self):
        # getting server
        server = self.ui.ui_pages.login_page.sql

        # requesting data
        data_manager = self.ui.ui_pages.data_page

        try:
            data, start_date, end_date = data_manager.request_data(server)

        except TimeoutError as err: # se der erro, provavelmente a conexao foi perdida
            self.connnectionErrorDialog()
            return None

        # updating data on processing screen
        self.ui.ui_pages.process_page.updateRawData(data)
        self.ui.ui_pages.process_page.updateDates(start_date, end_date)

        # force click on third screen (left menu)
        self.ui.left_menu.btn_process.click()

    @Slot(list)
    def updateDataHandles(self, processed_data : list[object]):
        screen = self.ui.ui_pages.visualization_page
        screen.updateDataHandles(processed_data)

    def connnectionErrorDialog(self):
        '''
        Janela de Dialogo quando ocorre algum problema na conexão SQL.
        '''
        self.ui.ui_pages.login_page.disconnectSQL()
        dialog = ImportDialog(
            title = 'Erro',
            message = 'Não foi possível se comunicar com o banco de dados',
            description='Certifique-se de que a conexão esteja estabelecida',
            parent = self
        )
        dialog.okClicked.connect(lambda: self.change_page(page = 0, button = self.ui.left_menu.btn_home))
        dialog.exec()


if __name__ == "__main__":
    # locale
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())