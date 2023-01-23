# IMPORT QT CORE
from qt_core import *

class UI_PyStationListView(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("station_manager")

        # SETTING STYLESHEET
        parent.setStyleSheet(f'''
            #station_manager {{
                border: none;
                background-color: transparent;
            }}
            QListWidget::item {{
                border: none;
                padding-left: 0px;
                padding-right: 0px;
            }}
            ''')
        