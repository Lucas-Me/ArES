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

        # SQL request
        self.ui.ui_pages.data_page.ui.sql_btn.clicked.connect(self.updateDatabaseSQL)

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
            dialog = ImportDialogSQL(self)
            dialog.show()
            return None

    
        # browser sql files
        self.ui.ui_pages.data_page.browse_sql(server)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())