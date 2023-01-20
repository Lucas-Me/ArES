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
        self.marked = CountMark(width=30, height=30)

        # animation properties
        self.animation = QPropertyAnimation()

        # Creating labels
        self.station_name_label = QLabel(self.station_object.metadata['name'])
        self.station_type_label = QLabel(self.station_object.metadata['type'])
        self.station_enterprise_label = QLabel(self.station_object.metadata['enterprise'])

        # Setup main UI
        self.ui = UI_StationListItem()
        self.ui.setup_ui(self)

    def change_color(self, color, highlight = False):
        if highlight:
            self.setStyleSheet(f'''
                background-color: {color};
                border: 3px solid;
                border-color: #88edd3;
            ''')

        else:
            self.setStyleSheet(f'''
                background-color: {color};
                border: none;
                border-bottom: 2px solid;
                border-left: 2px solid;
                border-right: 2px solid;
                border-color: #b7c4c8;
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
        

class CountMark(QWidget):

    def __init__(self, width, height, marked = 0, icon_color = '#fb8500', digit_color = '#ffffff'):
        super().__init__()

        # OBJECTS
        self.count_marked = marked
        self.icon_color = icon_color
        self.font = QFont('Open Sans', 10)
        self.pen = QPen()

        # SETTING UP PROPERTIES
        self.setFixedHeight(height)
        self.setFixedWidth(width)

        # CONFIGURING OBJECTS
        self.font.setBold(True)
        self.pen.setStyle(Qt.PenStyle.SolidLine)
        self.pen.setColor(QColor(digit_color))

    def updateCount(self, n):
        self.count_marked = n
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        
        # properties
        rect = self.rect()
        center = QPoint(self.width() // 2, self.height() // 2)
        r = rect.width() / 3
        
        # Setting up painter
        painter = QPainter(self)
        painter.save()
        painter.beginNativePainting()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.eraseRect(rect)
        if self.count_marked > 0:

            # PAINTING CIRCLE
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.icon_color)))
            painter.drawEllipse(center, r, r)

            # painting number
            painter.setFont(self.font)
            painter.setPen(self.pen)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self.count_marked))
            
        # Finishing Painter
        painter.endNativePainting()
        painter.restore()