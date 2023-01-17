# IMPORT QT CORE
from qt_core import *

# IMPORT MODULES
import os

# CUSTOM CHECKBOX CLASS
class PyRadioButton(QRadioButton):

    def __init__(
        self,
        height : int,
        width : int,
        text : str = ''
    ):
        super().__init__()
        
        # properties
        self.btn_height = height
        self.btn_width = width
        self.setText(text)

        # setting up style
        self.set_style()

    def set_style(self):
        # Folder and icon path
        app_path = os.path.abspath(os.getcwd())
        icons_folder = os.path.join(app_path, 'gui/images/icons')
        checked_path = os.path.normpath(os.path.join(icons_folder, 'icon_checkbox_checked.svg')).replace('\\', '/')
        unchecked_path = os.path.normpath(os.path.join(icons_folder, 'icon_checkbox_unchecked.svg')).replace('\\', '/')
        
        # Setting dimensions
        self.setMaximumHeight(self.btn_height)
        self.setMinimumHeight(self.btn_height)
        self.setMaximumWidth(self.btn_width)
        self.setMinimumWidth(self.btn_width)

        # setting Style sheet
        self.setStyleSheet(f'''
            QRadioButton::indicator {{
                width : {self.btn_width - 10}px;
                height: {self.btn_height - 10}px;
                padding-left: 5px; 
                vertical-align: middle;
                border: none none none none;
                background-color: none;
                border-radius: 0px;
                margin: 0px 0px 0px 0px;
            }}
            QRadioButton::indicator::unchecked {{
                image: url({unchecked_path});
            }}
            QRadioButton::indicator::checked {{
                image: url({checked_path});
            }}
        '''
        )

        return None
