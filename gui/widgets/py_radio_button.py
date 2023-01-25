# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

# IMPORT MODULES
import os

# CUSTOM CHECKBOX CLASS
class PyCheckButton(QCheckBox):
    checked = Signal()
    unchecked = Signal()

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
        self.setTristate(True)
        self.setCheckable(False)

        # setting up style
        self.set_style()
        
    def mousePressEvent(self, e: QMouseEvent) -> None:
        '''
        Sobrescreve o comportamento padrao do widget QCheckBox, ao ser clicado.
        '''

        state = self.checkState()
        if state != Qt.CheckState.Unchecked:
            self.setCheckState(Qt.CheckState.Unchecked)
            self.unchecked.emit()

        else:
            self.setCheckState(Qt.CheckState.Checked)
            self.checked.emit()

    def set_style(self):
        # Folder and icon path
        checked_path = get_imagepath('icon_checkbox_checked.svg', 'gui/images/icons')
        unchecked_path = get_imagepath('icon_checkbox_unchecked.svg', 'gui/images/icons')
        undetermined_path = get_imagepath('icon_checkbox_tristate.svg', 'gui/images/icons')

        # Setting dimensions
        self.setFixedSize(self.btn_width, self.btn_height)

        # setting Style sheet
        self.setStyleSheet(f'''
            QCheckBox::indicator {{
                width : {self.btn_width - 10}px;
                height: {self.btn_height - 10}px;
                padding-left: 5px; 
                vertical-align: middle;
                border: none none none none;
                background-color: none;
                border-radius: 0px;
                margin: 0px 0px 0px 0px;
            }}
            QCheckBox::indicator::unchecked {{
                image: url({unchecked_path});
            }}
            QCheckBox::indicator::checked {{
                image: url({checked_path});
            }}
            QCheckBox::indicator:indeterminate {{
                image: url({undetermined_path});
            }}
        '''
        )

        return None

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
        checked_path = get_imagepath('icon_checkbox_checked.svg', 'gui/images/icons')
        unchecked_path = get_imagepath('icon_checkbox_unchecked.svg', 'gui/images/icons')

        # Setting dimensions
        self.setFixedSize(self.btn_width, self.btn_height)

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