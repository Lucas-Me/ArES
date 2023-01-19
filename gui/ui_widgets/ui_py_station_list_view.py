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
            QScrollBar:vertical {{              
                border: none;
                background: #b7c4c8;
                width: 10px;
                border-radius: 5px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0 #fb8500, stop: 0.5 #fb8500, stop:1 #fb8500);
                min-height: 0px;
                width: 5px;
                border-width: 1px;
                border-radius: 5px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::add-line:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0 #fb8500, stop: 0.5 #fb8500, stop:1 #fb8500);
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                border-radius: 5px;
            }}
            QScrollBar::sub-line:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0 #fb8500, stop: 0.5 #fb8500, stop:1 #fb8500);
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            ''')
        
        # Sroll bar properties
        parent.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
