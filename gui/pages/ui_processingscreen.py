# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from backend.misc.functions import get_imagepath
from gui.widgets.parameter_summary import ParameterSummary, ParameterHeader
from gui.widgets.profile_picker import ProfilePicker

# Data Manager Page UI Class
class UI_ProcessScreen(object):
    
    def setup_ui(self, parent):
        
        # FRAME CONSTANTS
        parent.setObjectName(u'process_page')

        # MAIN LAYOUT
        self.main_layout = QGridLayout(parent)
        self.main_layout.setVerticalSpacing(20)
        self.main_layout.setHorizontalSpacing(20)
        self.main_layout.setContentsMargins(30, 20, 30, 20)

        # TOP LABEL
        # /////////////////////////////////////////////////////////////
        self.date_label = QLabel()
        self.date_label.setFixedHeight(35)
        self.date_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.date_label.setObjectName('date_label')
        
        # SETTINGS FRAME
        # ///////////////////////////////////////////////////////////////
        self.settings_frame = QFrame()
        self.settings_frame.setObjectName('settings_frame')
        self.settings_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.settings_frame.setFixedSize(200, 200)

        self.settings_layout = QVBoxLayout(self.settings_frame)
        self.settings_layout.setContentsMargins(10, 10, 10, 10)
        self.settings_layout.setSpacing(10)

        # TITLE
        self.settings_label = QLabel("Configurações")
        self.settings_label.setFixedHeight(25)
        self.settings_label.setObjectName('settings_label')
        self.settings_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ADD TO FRAME
        self.settings_layout.addWidget(self.settings_label, alignment = Qt.AlignmentFlag.AlignTop)
        
        # COMBOBOXES
        labels = ['Válidos', 'Inválidos', 'Suspeitos']
        names = ['validos', 'invalidos', 'suspeitos']
        self.checkbox_flags = []
        for i in range(len(labels)):
            box = QCheckBox(labels[i])
            box.setFixedWidth(self.settings_frame.width() - 20)
            box.setFixedHeight(30)
            box.setObjectName(names[i])
            #
            self.settings_layout.addWidget(box)
            self.checkbox_flags.append(box)

        self.checkbox_flags[0].setChecked(True)
        # SUMMARY FRAME
        # ///////////////////////////////////////////////////////////////
        self.summary_frame = QFrame()
        self.summary_frame.setObjectName('summary_frame')
        self.summary_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.summary_frame.setFixedHeight(200)

        # PROFILE FRAME
        # ////////////////////////////////////////////////////////////////
        self.profile_frame = QFrame()
        self.profile_frame.setObjectName('profile_frame')
        self.profile_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.profile_frame.setFixedSize(250, 200)

        self.profile_layout = QHBoxLayout(self.profile_frame)
        self.profile_layout.setContentsMargins(0, 0, 0, 0)
        self.profile_layout.setSpacing(0)

        self.profile_picker = ProfilePicker()
        self.profile_layout.addWidget(self.profile_picker)

        # PARAMETERS LIST
        # ////////////////////////////////////////////////////////////////////
        self.parameter_layout = QVBoxLayout()
        self.parameter_layout.setContentsMargins(0,0,0,0)
        self.parameter_layout.setSpacing(0)

        # Parameter Header
        self.header = ParameterHeader(height = 50)

        # Parameter List Widget
        self.parameter_list = ParameterSummary(item_height = 40)

        # Add to Parameter layout
        self.parameter_layout.addWidget(self.header)
        self.parameter_layout.addWidget(self.parameter_list)

        # MAIN LAYOUT CONFIGURATION
        # ////////////////////////////////////////////////////////////////

        # add to main layout
        self.main_layout.addWidget(self.date_label, 0, 0)
        self.main_layout.addWidget(self.settings_frame, 1, 0)
        self.main_layout.addWidget(self.summary_frame, 1, 1)
        self.main_layout.addWidget(self.profile_frame, 1, 2)
        self.main_layout.addLayout(self.parameter_layout, 2, 0, 1, 3)

        # alignment
        self.main_layout.setAlignment(self.date_label, Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setAlignment(self.settings_frame, Qt.AlignmentFlag.AlignTop)
        self.main_layout.setAlignment(self.summary_frame, Qt.AlignmentFlag.AlignTop)
        self.main_layout.setAlignment(self.profile_frame, Qt.AlignmentFlag.AlignTop)

    def setup_stylesheet(self, parent):
        # CONSTANTS
        font = 'Microsoft New Tai Lue'
        font_color = '#1c1c1c'
        bg_color = '#FAFAFA'
        border_radius = 10

        checked_path = get_imagepath('checked_mark.svg', 'gui/images/icons')
        unchecked_path = get_imagepath('unchecked_mark.svg', 'gui/images/icons')

        # UPPER LEFT STYLESHEET
        parent.setStyleSheet(f'''
            #process_page{{
                background-color: {bg_color};
            }}
            #profile_frame, #summary_frame, #settings_frame{{
                background-color: #ffffff;
                border-radius: {border_radius}px;
                border: 1px solid #cccccc;
            }}
            #total_label, #date_label{{
                background-color: #ffffff;
                font: 500 14pt '{font}';
                color: {font_color};
                border: 1px solid #cccccc;
                border-radius: {border_radius}px;
                text-align: left;
                padding-left: 10px;
            }}
            #settings_label {{
                font: 500 14pt '{font}';
                color: {font_color};
                border: none;
                text-align: left;
            }}
            #validos, #invalidos, #suspeitos {{
                background-color: #fafafa;
                font: 500 12pt '{font}';
                color: {font_color};
                border: 1px solid;
                border-radius: {border_radius}px;
                text-align: middle;
                padding-left: 10px;
            }}
            #validos::indicator:checked, #invalidos::indicator:checked, #suspeitos::indicator:checked {{
                image: url({checked_path});
            }}
            #validos:checked, #invalidos:checked, #suspeitos:checked {{
                border-color: #58aeee;
                color: #58aeee;
            }}
            #validos:checked:hover, #invalidos:checked:hover, #suspeitos:checked:hover {{
                background-color: #e4e4e4;
            }}
            #validos::indicator:unchecked, #invalidos::indicator:unchecked, #suspeitos::indicator:unchecked {{
                image: url({unchecked_path});
            }}
            #validos:unchecked, #invalidos:unchecked, #suspeitos:unchecked {{
                border-color: #5c5c5c;
                color: #5c5c5c;
            }}
            #validos:unchecked:hover, #invalidos:unchecked:hover, #suspeitos:unchecked:hover {{
                background-color: #e4e4e4;
            }}
        ''')

    