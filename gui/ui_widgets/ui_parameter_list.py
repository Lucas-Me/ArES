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
                border: 1px solid;
                border-color: #000000;
            }}
            QListWidget::item {{
                border-bottom: 1px solid;
                border-color: #000000;
            }}
            ''')

        # SCROLL BAR PROPERTIES
        parent.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)