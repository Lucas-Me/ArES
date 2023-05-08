# QT MODULES
import PySide6.QtGui
from qt_core import *

# IMPORTING MODULES
import numpy as np

# IMPORT CUSTOM MODULES
from gui.windows.dialog.legend.color_dialog import LegendDialog


def calculateLuminance(rgb : np.array):
    # Calculate luminance of a color
    rgb = np.array(rgb)
    rgb2 = np.where(rgb <= 10, rgb / 3294, (rgb / 269 + 0.0513) ** 2.4)

    # Luminance
    L = np.sum(rgb2 * np.array([0.2126, 0.7152, 0.0722]))

    return L

def getContrast(color : str):
    # Calculate contrast between the selected color and (black, white)
    L1 = calculateLuminance(QColor(color).getRgb()[:-1])
    L2 = calculateLuminance(QColor('white').getRgb()[:-1])

    # CONTRAST RATIO BETWEEN THE COLOR AND WHITE
    contrast_ratio = (L1 + 0.05) / (L2 + 1.05)
    minimum_contrast_ratio = 0.5
    final_color = "#000000" if contrast_ratio > minimum_contrast_ratio else '#ffffff'
    
    return QColor(final_color)

class ColormapWidget(QFrame):

    def __init__(self, *args, **kwargs):
        # PRIVATE VARIABLES
        self.gradient_ = QLinearGradient()
        self.colors = [] # list of colors

        # INIT
        super().__init__(*args, **kwargs)

        # SETUP UI
        self.ui = ViewerUI()
        self.ui.setup_ui(self)

        # settings
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.gradient_.setCoordinateMode(QGradient.ObjectBoundingMode)

        # init
        self.refreshColors(["#ffffff", '#000000'])
        self.refreshItems()
        self.setFixedHeight(40)

    def paintEvent(self, event: QPaintEvent) -> None:
        # super().paintEvent()

        # creating painter
        painter = QPainter()
        painter.begin(self)

        # painting box
        painter.fillRect(QRect(0, 0, self.width(), self.height()), self.gradient_)
        painter.end()

    def refreshColors(self, colors):
        self.gradient_ = QLinearGradient()
        self.gradient_.setStart(0, 0)
        self.gradient_.setFinalStop(1, 0)
        self.gradient_.setCoordinateMode(QGradient.ObjectBoundingMode)
        self.colors = colors

        # adding colors
        n = len(colors)
        positions = np.linspace(0, 1, n)
        for i in range(n):
            self.gradient_.setColorAt(positions[i], colors[i])

        # update colormap
        self.update()

    def refreshItems(self):
        # removing children
        n = self.ui.main_layout.count()
        for i in range(n):
            self.ui.main_layout.itemAt(i).widget().deleteLater()
            self.ui.main_layout.takeAt(i)

        # adding elements
        for i in range(len(self.colors)):
            if i > 0:
                self.ui.main_layout.addItem(
                    QSpacerItem(30, 30, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
                )

            # adding marker
            marker = ColorMarker(position = i, parent = self)
            marker.clicked.connect(self.editColor)
            self.ui.main_layout.addWidget(marker)

    def editColor(self, position):
        color = self.colors[position]
        print(position, color)

class ViewerUI(object):

    def setup_ui(self, parent : ColormapWidget):

        if not parent.objectName():
            parent.setObjectName("colormap")

        # MAIN LAYOUT
        self.main_layout = QHBoxLayout(parent)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)


class ColorMarker(QWidget):

    clicked = Signal(int)
    def __init__(self, position : int, parent : ColormapWidget):

        # INIT
        super().__init__(parent)

        # PRIVATE VARIABLES
        self.position = position

        # SETTINGS
        self.setFixedWidth(10)
        # self.setStyleSheet('background-color: red;')

    def mousePressEvent(self, event: QMouseEvent) -> None:
        ''' Emite um sinal ao ser clicado'''
        super().mousePressEvent(event)
        self.clicked.emit(self.position)
        
    def paintEvent(self, event: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        p.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

        # widget properties
        w = self.width()
        h = self.height()

        # MARKER PROPERTIES
        marker_h  = h // 4
        midpoint = w // 2

        # upper marker coords
        upper_marker = [
            QPointF(0, 0),
            QPointF(w, 0),
            QPointF(midpoint, marker_h),
            ]

        # lower marker coords
        lower_marker = [
            QPointF(0, h),
            QPointF(w, h),
            QPointF(midpoint, h - marker_h),
        ]

        # DRAWING
        color = getContrast(self.parent().colors[self.position])
        p.setBrush(QBrush(color))
        p.setPen(color)
        p.drawPolygon(upper_marker)
        p.drawPolygon(lower_marker)

        # END
        p.end()

