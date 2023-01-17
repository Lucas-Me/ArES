# IMPORT QT CORE
from qt_core import *

# Import Custom Widget
from gui.widgets.station_close_button import StaticButton

class UI_StationListItem(object):
    def setup_ui(
        self,
        parent : QFrame,
        background_color : str = "#ffffff",
    ):
        if not parent.objectName():
            parent.setObjectName(u'station_item')
        
        # SET INITIAL PARAMETERS
        parent.setMinimumHeight(parent.item_height - 5)
        parent.setMaximumHeight(parent.item_height - 5)
        parent.setMaximumWidth(parent.item_width)
        parent.setMinimumWidth(parent.item_width)
        parent.setStyleSheet(f'''
            background-color: {background_color};
        ''')

        # CREATE MAIN LAYOUT
        self.item_main_layout = QHBoxLayout(parent)
        self.item_main_layout.setContentsMargins(0, 0, 0, 0)
        self.item_main_layout.setSpacing(0)
        
        # CREATE CONTENT LAYOUT
        # ///////////////////////////////////////////////////////////////////

        # CREATE CONTENT LAYOUT
        self.item_content_layout = QVBoxLayout()

        # ADD TOP SPACER TO CONTENT LAYOUT
        self.item_content_top_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.item_content_layout.addItem(self.item_content_top_spacer)

        # FORMATING LABEL STYLE
        fontStyleSheet = """
            font-family : 'Microsoft New Tai Lue';
            padding-left : 10px;
            border: none;
        """
        for qlabel in [
            parent.station_name_label,
            parent.station_type_label,
            parent.station_enterprise_label
        ]:
            qlabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            qlabel.setMinimumHeight(20)
            qlabel.setMaximumHeight(20)
            f = qlabel.font()
            f.setHintingPreference(QFont.HintingPreference.PreferNoHinting);
            qlabel.setFont(f)

        parent.station_name_label.setStyleSheet(fontStyleSheet + '''
            font-weight: bold;
            font-size: 12pt;
        ''')

        parent.station_type_label.setStyleSheet(fontStyleSheet + '''
            font-size: 9pt;
        ''')
        parent.station_type_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        parent.station_enterprise_label.setStyleSheet(fontStyleSheet + '''
            font-size: 9pt;
        ''')

        # CREATING FIRST STATION INFO LINE
        self.station_label_layout = QHBoxLayout()

        # CREATING SPACER
        self.station_label_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # ADD LABELS TO STATION LABEL LAYOUT CONTENT LAYOUT
        self.station_label_layout.addWidget(parent.station_name_label)
        self.station_label_layout.addItem(self.station_label_spacer)
        self.station_label_layout.addWidget(parent.station_type_label)
        
        # ADD LABELS TO CONTENT LAYOUT
        self.item_content_layout.addLayout(self.station_label_layout)
        self.item_content_layout.addWidget(parent.station_enterprise_label)

        # ADD BOTTOM SPACER TO CONTENT LAYOUT
        self.item_content_bottom_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.item_content_layout.addItem(self.item_content_bottom_spacer)

        # ADD CONTENT LAYOUT TO MAIN LAYOUT
        self.item_main_layout.addLayout(self.item_content_layout)

        # CREATE RIGHT BAR
        # ///////////////////////////////////////////////////////////////////

        # RIGHT BAR LAYOUT
        self.right_bar_layout = QVBoxLayout()
        # self.right_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.right_bar_layout.setSpacing(0)

        # CREATING CLOSE BUTTON
        self.close_button = StaticButton(
            btn_height=30,
            btn_width=30,
            icon_path="icon_close_button.svg",
            btn_color= 'transparent',
            btn_hover= 'transparent',
            btn_pressed= 'transparent',
            icon_width=30,
            icon_height=30)

        # RIGHT BAR SPACER
        self.right_bar_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # ADD TO RIGHT BAR LAYOUT
        self.right_bar_layout.addWidget(self.close_button)
        self.right_bar_layout.addItem(self.right_bar_spacer)
        
        # INSERT RIGHT BAR TO MAIN LAYOUT
        self.item_main_layout.addLayout(self.right_bar_layout)

        



        