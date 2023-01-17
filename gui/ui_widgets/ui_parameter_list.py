# IMPORT QT CORE
from qt_core import *

class UI_ParameterSelection(object):

    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("Parameter List")

        # SETTING STYLESHEET
        self.scroll_bar_color = '#2874bf'
        parent.setStyleSheet(f'''
            QListWidget {{
                border: none;
            }}
            QListWidget::item {{
                border: none;
                padding-left: 10px;
                padding-right: 30px;
            }}
            QScrollBar:vertical {{              
                border: none;
                background: white;
                width: 10px;
                border-radius: 5px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0 {self.scroll_bar_color}, stop: 0.5 #1e588f, stop:1 {self.scroll_bar_color});
                min-height: 0px;
                width: 5px;
                border-width: 1px;
                border-radius: 5px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::add-line:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0 {self.scroll_bar_color}, stop: 0.5 #1e588f,  stop:1 {self.scroll_bar_color});
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                border-radius: 5px;
            }}
            QScrollBar::sub-line:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0  {self.scroll_bar_color}, stop: 0.5 #1e588f,  stop:1 {self.scroll_bar_color});
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            ''')

        # SCROLL BAR PROPERTIES
        parent.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)