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
                border: 0.5px solid;
                border-color: #6c8194;
            }}
            QListWidget::item {{
                border-bottom: 0.5px solid;
                border-color: #6c8194;
            }}
            ''')

        # SCROLL BAR PROPERTIES
        parent.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)