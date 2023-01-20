# IMPORT QT CORE
from qt_core import *

class UI_PyStationListView(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("StationListViewer")

        # setting properties
        self.scroll_bar_color = '#2874bf'
        self.background_color = '#4969b2'
        self.secondary_color = "#ffffff"

        # SETTING STYLESHEET
        parent.setStyleSheet(f'''
            QListWidget {{
                border: none;
                background-color: {self.background_color};
            }}
            QListWidget::item {{
                border: none;
                padding-left: 0px;
                padding-right: 0px;
            }}
            ''')
        