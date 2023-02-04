# IMPORT MODULES
import sys
import os

# IMPORT QT CORE
from qt_core import *

# IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import *

# IMPORT DIALGO
from gui.windows.dialog.import_dialog import ImportDialogSQL

# MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # window title
        self.setWindowTitle("ArES")

        # SETUP MAIN WINDOW
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # SIGNALS AND SLOTS
        # open page 1
        self.ui.btn_1.clicked.connect(lambda: self.change_page(page = 0, button = self.ui.btn_1))
        
        # open page 2
        self.ui.btn_2.clicked.connect(lambda: self.change_page(page = 1, button = self.ui.btn_2))

        # open page 3
        self.ui.btn_3.clicked.connect(lambda: self.change_page(page = 2, button = self.ui.btn_3))

        # SQL request
        self.ui.ui_pages.data_page.ui.sql_btn.clicked.connect(self.updateDatabaseSQL)

        # NEXT button on DATA MANAGER SCREEEn
        self.ui.ui_pages.data_page.ui.next_btn.clicked.connect(self.requestData)

        # EXIBE A APLICAÇÃO
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
            self.ui.ui_pages.login_page.disconnectSQL()
            dialog = ImportDialogSQL(self)
            dialog.show()
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

        except Exception as err: # se der erro, provavelmente a conexao foi perdida
            print(err)
            self.ui.ui_pages.login_page.disconnectSQL()
            dialog = ImportDialogSQL(self)
            dialog.show()
            return None

        # updating data on processing screen
        self.ui.ui_pages.process_page.updateRawData(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())