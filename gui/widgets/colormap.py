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
        self.setFixedHeight(60)

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
        self.border_length = 5
        self.levels = Levels(border_length = self.border_length)

        # INITs
        super().__init__()

        # SETUP UI
        self.setup_ui()

        # settings
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        # init
        self.refreshItems(kwargs.get("colors", ["#ffffff", '#000000']))
        self.setFixedHeight(80)
    
    def setup_ui(self):

        if not self.objectName():
            self.setObjectName("colormap")

        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # UPPER LAYOUT (CORES)
        self.upper_layout = QHBoxLayout()
        self.upper_layout.setContentsMargins(self.border_length, 0, self.border_length, 0)
        self.upper_layout.setSpacing(0)

        # LOWER LAYOUT (INTERVALOS)
        self.main_layout.addLayout(self.upper_layout)
        self.main_layout.addWidget(self.levels)

    def refreshItems(self, colors):
        # removing children
        n = self.upper_layout.count()
        for i in reversed(range(n)):
            item = self.upper_layout.itemAt(i)
            if item.spacerItem():
                self.upper_layout.removeItem(item)
                del item
            else:
                item.widget().deleteLater()
                self.upper_layout.takeAt(i)

        # cleaning list
        self.colorMarkers.clear()

        # garbage collector
        gc.collect()

        # adding elements
        for i in range(len(colors)):
            self.insertMarker(color = colors[i], update_levels = False)

        # updating levels
        self.levels.setLevels(np.arange(0, len(colors) + 1))
        self.levels.update()

    def editColor(self, marker):
        dialog = ColorEditDialog(marker)
        dialog.loadContents()
        dialog.show()

    def removeColor(self, marker):
        # get index
        index = self.colorMarkers.index(marker)
        self.colorMarkers.pop(index)

        # remove object
        item = self.upper_layout.itemAt(index)
        item.widget().deleteLater()
        self.upper_layout.takeAt(index)

        # updating ticks
        self.levels.updateLevels(len(self.colorMarkers) + 1)

    def updateColor(self, marker, color_name):
        marker.setColor(color_name)
    
    def getColors(self):
        return [marker.getColor() for marker in self.colorMarkers]
    
    def insertMarker(self, color, update_levels = True):
        # adding marker
        marker = DiscreteColorMarker(color = color, parent = self)
        marker.doubleClick.connect(self.editColor)
        marker.rightClick.connect(self.removeColor)
        self.colorMarkers.append(marker)
        self.upper_layout.addWidget(marker)

        if update_levels:
            # updating ticks
            self.levels.updateLevels(len(self.colorMarkers) + 1)

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


class Levels(QFrame):
    """Classe que mostra os níveis dos intervalos relacionados
    a um esquema de cores discreto (discrete colormap).
    De preferencia, posicionado logo abaixo do colormap"""

    def __init__(self, border_length, levels = [1, 2]):

        # PRIVATE VARIABLES
        self.levels = levels
        self.border_length = border_length
        self.pen = QPen()
        self.font = QFont()

        # INIT
        super().__init__(parent= None)

        # SETTINGS
        self.pen.setColor("#000000")
        self.pen.setWidth(3)
        # self.font.setBold(True)
        self.font.setPixelSize(12)
        self.setFixedHeight(20)

    def setLevels(self, levels):
        if not isinstance(levels, list):
            levels = levels.tolist()

        self.levels = levels
        self.update()

    def getLevels(self):
        return self.levels
    
    def updateLevels(self, n):
        levels = self.getLevels() # esta em ordem crescente
        vmax, vmin = levels[-1], levels[0]
        self.setLevels(np.round(np.linspace(vmin, vmax, n), 1))
    
    def paintEvent(self, event: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        p.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

        # widget properties and pen settings
        tick_height = 3
        p.setPen(self.pen)
        p.setFont(self.font)

        # DRAWING LEVELS
        n = len(self.levels)
        positions = np.round(np.linspace(0 + self.border_length, self.width() - self.border_length, n), 0).astype(int)
        dx = (positions[-1] - positions[0]) // n
        positions[0] += self.border_length // 2
        positions[-1] -= self.border_length // 2

        for i in range(n):
            p1 = QPoint(positions[i], 0) # ponto superior
            p2 = QPoint(positions[i], tick_height) # ponto inferior

            # draw tick
            p.drawLine(p1, p2)

            # draw value
            p.drawText(
                QRectF(positions[i] - dx // 2, 0, dx, self.height()),
                str(self.levels[i]),
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom
                )

        # END
        p.end()