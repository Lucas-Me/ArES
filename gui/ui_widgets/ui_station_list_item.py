# IMPORT QT CORE
from qt_core import *

class UI_StationListItem(object):
    def setup_ui(self, parent : QFrame):
        if not parent.objectName():
            parent.setObjectName(u'station_item')
        
        # CREATE MAIN LAYOUT
        self.main_layout = QHBoxLayout(parent)
        self.main_layout.setContentsMargins(0, 0, 10, 0)
        self.main_layout.setSpacing(10)
        
        # SIGNATURE FRAME
        # /////////////////////////////////////////////////
        self.signature_frame = QFrame()
        self.signature_frame.setObjectName('signature')
        self.signature_frame.setFixedWidth(10)
        
        # LABELS
        # //////////////////////////////////////////////////
        self.station_name = QLabel(parent._name)
        self.station_name.setObjectName('name_label')
        self.station_name.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.station_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        #
        self.station_type = QLabel(parent._type)
        self.station_type.setObjectName('type_label')
        self.station_type.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.station_type.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # label layout
        self.label_layout = QVBoxLayout()
        self.label_layout.setContentsMargins(0, 5, 0, 5)
        self.label_layout.setSpacing(5)

        # add to label layout
        self.label_layout.addWidget(self.station_name)
        self.label_layout.addWidget(self.station_type)

        # CONFIGURING MAIN LAYOUT
        # ///////////////////////////////////////////////////////////////////
        self.main_layout.addWidget(self.signature_frame)
        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addWidget(parent.marked)

        # CREATE RIGHT BAR IF OBJECT CAME FROM AN XLS FILE
        # ///////////////////////////////////////////////////////////////////
        if parent.is_xls():
            # CREATING DELETE BUTTON
            self.delete_btn = QPushButton("X")
            self.delete_btn.setObjectName('delete_btn')
            self.delete_btn.setFixedSize(20, 20)

            self.main_layout.addWidget(self.delete_btn)
            self.main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # SETTING UP STYLESHEET
        self.station_name.updateGeometry()
        self.station_type.updateGeometry()
        self.setup_stylesheet(parent)
    
    def setup_stylesheet(self, parent):
        font = 'Microsoft New Tai Lue'
        font_color_1 = '#32495e'
        font_color_2 = '#6c8194'
        frame_color = '#398e3d' if parent.is_xls() else '#008299'
        parent.setStyleSheet(f'''
            #station_item {{
                background-color: #ffffff;
            }}
            #signature {{
                background-color: {frame_color};
                border: none;
            }}
            #name_label {{
                background-color: transparent;
                border: none;
                color: {font_color_1};
                font: 500 13pt {font};
            }}
            #type_label {{
                background-color: transparent;
                border: none;
                color: {font_color_2};
                font: 500 13pt {font};
            }}
            #delete_btn {{
                background-color: #6c8194;
                color: #ffffff;
                font: bold 12pt {font};
                border: none;
            }}
            #delete_btn:hover {{
                background-color: #f53c00;
            }}
            #delete_btn:pressed{{
                background-color: #c43305;
            }}
        '''
        )



        