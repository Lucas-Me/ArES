# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.ui_widgets.ui_station_list_item import UI_StationListItem

class StationListItem(QFrame):

    def __init__(
        self,
        station_object, 
        item_width : int = 380,
        item_height : int = 60,
    ) -> None:
        super().__init__()

        # PROPERTIES
        self.marked = CountMark(width=30, height=30)
        self._signature = station_object.metadata['signature']
        self._name = station_object.metadata['name']
        self._type = station_object.metadata['type']
        self._xls = self._signature[:3] == 'xls'

        # CONFIGURATION
        self.setFixedSize(QSize(item_width, item_height))

        # SETUP UI
        self.ui = UI_StationListItem()
        self.ui.setup_ui(self)

    def is_xls(self):
        return self._xls

    def change_color(self, color, highlight = False):
        style  = self.styleSheet()
        if highlight:
            self.setStyleSheet(style + f'''
                #station_item {{
                    background-color: {color};
                }}
            ''')

        else:
            self.setStyleSheet(style + f'''
                #station_item {{
                    background-color: #ffffff;
                }}
            ''')


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
        
        if self.count_marked > 0:

            # Setting up painter
            painter = QPainter(self)
            painter.save()
            painter.beginNativePainting()
            painter.setRenderHint(QPainter.Antialiasing)

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