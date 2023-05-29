# QT MODULES
from qt_core import *

# IMPORT BUILT-IND MODULES
import gc

# IMPORTING MODULES
import numpy as np

# IMPORT CUSTOM MODULES
from gui.windows.dialog.legend.color_dialog import ColorEditDialog


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
        self.gradient_ = LinearGradient()
        self.color_markers = [] # list of color markers

        # INIT
        super().__init__()

        # SETUP UI
        self.ui = ViewerUI()
        self.ui.setup_ui(self)

        # settings
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.gradient_.setCoordinateMode(QGradient.ObjectBoundingMode)

        # init
        self.refreshItems(kwargs.get("colors", ["#ffffff", '#000000']))
        self.refreshColors()
        self.setFixedHeight(40)

    def paintEvent(self, event: QPaintEvent) -> None:
        # super().paintEvent()

        # creating painter
        painter = QPainter()
        painter.begin(self)

        # painting box
        painter.fillRect(QRect(0, 0, self.width(), self.height()), self.gradient_)

        # BORDER
        pen =  QPen()
        pen.setColor("#000000")
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRect(self.rect())

        # END
        painter.end()

    def refreshColors(self):
        self.gradient_ = LinearGradient()
        self.gradient_.setStart(0, 0)
        self.gradient_.setFinalStop(1, 0)
        self.gradient_.setCoordinateMode(QGradient.ObjectBoundingMode)
        colors = self.getColors()

        # adding colors
        n = len(colors)
        positions = np.linspace(0, 1, n)
        for i in range(n):
            self.gradient_.setColorAt(positions[i], colors[i])

        # update colormap
        self.update()

    def refreshItems(self, colors):
        # removing children
        n = self.ui.main_layout.count()
        for i in reversed(range(n)):
            item = self.ui.main_layout.itemAt(i)
            if item.spacerItem():
                self.ui.main_layout.removeItem(item)
                del item
            else:
                item.widget().deleteLater()
                self.ui.main_layout.takeAt(i)

        # cleaning list
        self.color_markers.clear()

        # garbage collector
        gc.collect()

        # adding elements
        for i in range(len(colors)):
            if i > 0:
                self.ui.main_layout.addItem(
                    QSpacerItem(30, 30, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
                )

            # adding marker
            marker = ColorMarker(color = colors[i], parent = self)
            marker.leftClick.connect(self.editColor)
            marker.rightClick.connect(self.removeColor)
            self.color_markers.append(marker)
            self.ui.main_layout.addWidget(marker)

    def editColor(self, marker):
        dialog = ColorEditDialog(marker)
        dialog.loadContents()
        dialog.show()

    def removeColor(self, marker):
        n = len(self.color_markers)

        if n > 2:
            self.color_markers.remove(marker)
            self.refreshItems(self.getColors())
            self.refreshColors()

    def updateColor(self, marker, color_name):
        marker.setColor(color_name)
        self.refreshColors()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        # getting position of the click
        self.insertMarker(len(self.color_markers) + 1)
        return super().mouseDoubleClickEvent(event)
    
    def getColors(self):
        return [marker.getColor() for marker in self.color_markers]
    
    def insertMarker(self, nmarkers):
        # deducing new colors
        positions = np.linspace(0, 1, nmarkers)
        new_colors = [self.gradient_.getColor(position).name() for position in positions]
        self.refreshItems(new_colors)
        self.refreshColors()


class ViewerUI(object):

    def setup_ui(self, parent : ColormapWidget):

        if not parent.objectName():
            parent.setObjectName("colormap")

        # MAIN LAYOUT
        self.main_layout = QHBoxLayout(parent)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)


class ColorMarker(QWidget):

    leftClick = Signal(object)
    rightClick = Signal(object)
    def __init__(self, color : str, parent : ColormapWidget):

        # INIT
        super().__init__(parent)

        # PRIVATE VARIABLES
        self.color = QColor(color)

        # SETTINGS
        self.setFixedWidth(10)

    def getColor(self):
        return self.color.name()
    
    def setColor(self, color : str):
        self.color = QColor(color)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        ''' Emite um sinal ao ser clicado'''
        if event.button() == Qt.RightButton:
            self.rightClick.emit(self)
        else:
            self.leftClick.emit(self)

        super().mousePressEvent(event)
        
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

        # FILL COLOR
        color = getContrast(self.color.name())
        p.setBrush(QBrush(color))

        # BORDER COLOR
        pen =  QPen()
        pen.setColor("#000000")
        pen.setWidth(1)
        p.setPen(pen)

        # DRAW POLYGON
        p.drawPolygon(upper_marker)
        p.drawPolygon(lower_marker)

        # END
        p.end()


class LinearGradient(QLinearGradient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # PROPERTIES
        self.ncolors = 0
        self.mGradientColors = []
    
    def getColor(self, value):
        # Assume mGradientColors.count()>1 and value=[0,1]
        interval= self.ncolors - 1 
        stepbase = 1.0 / interval

        for i in range(1, self.ncolors):
            if value <= i * stepbase:
                interval = i
                break

        percentage = (value-stepbase*(interval-1))/stepbase
        color = self.interpolate(self.mGradientColors[interval], self.mGradientColors[interval-1], percentage)        
        return color

    def interpolate(self, start : QColor, end : QColor, ratio : float):
        r = int((ratio*start.red() + (1-ratio)*end.red()))
        g = int((ratio*start.green() + (1-ratio)*end.green()))
        b = int((ratio*start.blue() + (1-ratio)*end.blue()))

        return QColor.fromRgb(r,g,b)

    def setColorAt(self, pos: float, color) -> None:
        self.ncolors += 1
        self.mGradientColors.append(QColor(color))

        return super().setColorAt(pos, color)
    

class DiscreteColormap(QFrame):
        
    def __init__(self, *args, **kwargs):
        # PRIVATE VARIABLES
        self.colorMarkers = [] # list of color markers

        # INITs
        super().__init__()

        # SETUP UI
        self.ui = ViewerUI()
        self.ui.setup_ui(self)

        # settings
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        # init
        self.refreshItems(kwargs.get("colors", ["#ffffff", '#000000']))
        self.setFixedHeight(40)
        
    def refreshItems(self, colors):
        # removing children
        n = self.ui.main_layout.count()
        for i in reversed(range(n)):
            item = self.ui.main_layout.itemAt(i)
            if item.spacerItem():
                self.ui.main_layout.removeItem(item)
                del item
            else:
                item.widget().deleteLater()
                self.ui.main_layout.takeAt(i)

        # cleaning list
        self.colorMarkers.clear()

        # garbage collector
        gc.collect()

        # adding elements
        for i in range(len(colors)):
            self.insertMarker(color = colors[i])

    def editColor(self, marker):
        dialog = ColorEditDialog(marker)
        dialog.loadContents()
        dialog.show()

    def removeColor(self, marker):
        pass
        # colors = self.colors
        # n = len(self.colors)

        # if n > 2:
        #     colors.pop(position)
        #     self.refreshColors(self.colors)
        #     self.refreshItems()

    def updateColor(self, marker, color_name):
        marker.setColor(color_name)
    
    def getColors(self):
        return [marker.getColor() for marker in self.colorMarkers]
    
    def insertMarker(self, color):
        # adding marker
        marker = DiscreteColorMarker(color = color, parent = self)
        marker.doubleClick.connect(self.editColor)
        marker.rightClick.connect(self.removeColor)
        self.colorMarkers.append(marker)
        self.ui.main_layout.addWidget(marker)


class DiscreteColorMarker(QFrame):

    doubleClick = Signal(object)
    rightClick = Signal(object)
    def __init__(self, color : str, parent : ColormapWidget):

        # INIT
        super().__init__(parent)

        # PRIVATE VARIABLES
        self.color = QColor(color)

        # SETTINGS
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        # self.setStyleSheet('background-color: red;')

    def setColor(self, color):
        self.color = QColor(color)
        self.update()

    def getColor(self):
        return self.color.name()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        ''' Emite um sinal ao ser clicado duas vezes'''
        self.doubleClick.emit(self)

        super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        ''' Emite um sinal ao ser clicado uma vez com o botão direito'''
        if event.button() == Qt.RightButton:
            self.rightClick.emit(self)

        return super().mousePressEvent(event)
    
    def paintEvent(self, event: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        p.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

        # widget propertie
        rect = self.rect()

        # DRAWING
        p.setBrush(QBrush(self.color))
        pen = QPen()
        pen.setColor("#000000")
        pen.setWidth(4)
        p.setPen(pen)
        p.fillRect(rect, p.brush())
        p.drawRect(rect)

        # END
        p.end()

