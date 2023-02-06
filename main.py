# IMPORT MODULES
import sys
import mysql.connector

# IMPORT QT CORE
from qt_core import *

# IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import *

# IMPORT DIALGO
from gui.windows.dialog.import_dialog import ImportDialogSQL
from gui.windows.loading.splash_screen import SplashScreen


class LoadUi(QObject):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.mainWindow = parent

    @Slot()
    def start(self):
        # load the main UI
        self.mainWindow.ui = UI_MainWindow()
        self.mainWindow.ui.setup_ui(self.mainWindow)

        # open page 1
        self.mainWindow.ui.btn_1.clicked.connect(lambda: self.mainWindow.change_page(page = 0, button = self.mainWindow.ui.btn_1))
        
        # open page 2
        self.mainWindow.ui.btn_2.clicked.connect(lambda: self.mainWindow.change_page(page = 1, button = self.mainWindow.ui.btn_2))

        # open page 3
        self.mainWindow.ui.btn_3.clicked.connect(lambda: self.mainWindow.change_page(page = 2, button = self.mainWindow.ui.btn_3))

        # SQL request
        self.mainWindow.ui.ui_pages.data_page.ui.sql_btn.clicked.connect(self.mainWindow.updateDatabaseSQL)

        # NEXT button on DATA MANAGER SCREEEn
        self.mainWindow.ui.ui_pages.data_page.ui.next_btn.clicked.connect(self.mainWindow.requestData)

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
        # self.loadUI.moveToThread(self.uiLoadingThread)

        # SIGNALS AND SLOTS
        # connect the ui loaded signal
        self.uiLoaded.connect(self.closeLoadingScreen)

        # connet the start
        self.uiLoadingThread.started.connect(self.loadUI.start)
        
        # Start the UI Loading
        self.uiLoadingThread.start()

    
    def closeLoadingScreen(self):
        # Close the loading screen
        self.loadingScreen.close()

        # show the main UI
        self.show()

    def reset_menu_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            btn.set_active(False)

    def change_page(self, page : int, button : QPushButton):
        self.reset_menu_selection()
        self.ui.pages.setCurrentIndex(page)
        button.set_active(True)

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
            data = data_manager.request_data(server)

        except mysql.connector.Error as err: # se der erro, provavelmente a conexao foi perdida
            print(err)
            self.connnectionErrorDialog()
            return None

        # updating data on processing screen
        self.ui.ui_pages.process_page.updateRawData(data)

    def connnectionErrorDialog(self):
        '''
        Janela de Dialogo quando ocorre algum problema na conexão SQL.
        '''
        self.ui.ui_pages.login_page.disconnectSQL()
        dialog = ImportDialogSQL(self)
        dialog.okClicked.connect(lambda: self.change_page(page = 0, button = self.ui.btn_1))
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())