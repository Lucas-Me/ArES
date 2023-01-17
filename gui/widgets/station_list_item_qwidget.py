# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.ui_widgets.ui_station_list_item import UI_StationListItem

class StationListItem(QFrame):

    def __init__(
        self,
        station_object, 
        item_width : int = 380,
        item_height : int = 60   
    ) -> None:
        super().__init__()

        # Setting up properties
        self.station_object = station_object
        self.item_width = item_width
        self.item_height = item_height

        # animation properties
        self.animation = QPropertyAnimation()

        # Creating labels
        self.station_name_label = QLabel(self.station_object.metadata['name'])
        self.station_type_label = QLabel(self.station_object.metadata['type'])
        self.station_enterprise_label = QLabel(self.station_object.metadata['enterprise'])

        # Setup main UI
        self.ui = UI_StationListItem()
        self.ui.setup_ui(self)

    def change_color(self, color):
        self.setStyleSheet(f'''
            background-color: {color};
        ''')

    def insert_animation(self):
        # get current position and dimensions
        x = self.pos().x()
        y = self.pos().y()
        dx = self.width()
        dy = self.height()

        # estimate initial position
        x0 = x + dx / 2
        y0 = y + dy / 2

        # Creating animation
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b"geometry")
        self.animation.setStartValue(QRect(x0, y0, 0, 0))
        self.animation.setEndValue(QRect(x, y, dx, dy))
        self.animation.setDuration(300) # em milisegundos
        self.animation.setEasingCurve(QEasingCurve.OutCirc)
        self.animation.start()
        